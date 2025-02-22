from aws_cdk import (
    Stack,
    aws_ec2,
    aws_ecs,
    aws_elasticloadbalancingv2,
    aws_route53,
    aws_route53_targets,
    aws_certificatemanager,
    aws_ecr,
    aws_cloudfront,
    aws_cloudfront_origins,
    Duration,
)
from constructs import Construct

DOMAIN = "YOUR_DOMAIN_NAME"
EXTERNAL_SUBDOMAIN = "api"
# will be used to access our API via Cloudfront
# Having Cloudfront as an entry point is beneficial - it can be used to setup request caching,
# or for latency-based region selection in multi-region setups: https://aws.amazon.com/blogs/networking-and-content-delivery/latency-based-routing-leveraging-amazon-cloudfront-for-a-multi-region-active-active-architecture/
# or to have custom routing rules etc.

INTERNAL_SUBDOMAIN = "api-int"

# CDK AWS docs: https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_ecs-readme.html

class ApiStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create a VPC with 2 AZ (AvailabilityZones). Both AZ are located in the same region.
        # If one AZ goes down, the second will still serve API requests
        # By default each AZ in VPC contains 1 public and 1 private subnet
        # What is VPC: https://docs.aws.amazon.com/vpc/latest/userguide/what-is-amazon-vpc.html
        # What is Availability Zone: https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-regions-availability-zones.html
        vpc = aws_ec2.Vpc(
            self, "BackendAPIVpc",
            max_azs=2,  # Two availability zones
        )

        # Create an ECS cluster in our VPC
        # This cluster manages our service, e.g. launch tasks (task==service instance), check health etc.
        cluster = aws_ecs.Cluster(
            self, "BackendAPICluster",
            vpc=vpc,
        )

        # Define the smallest available FargateTask to host our backend
        # Fargate is a modern way to allocate tasks: https://docs.aws.amazon.com/AmazonECS/latest/developerguide/AWS_Fargate.html
        task_definition = aws_ecs.FargateTaskDefinition(
            self, "MyTask",
            cpu=256, #.25 vCPU
            memory_limit_mib=512 #0.5 GB
        )

        # Reference tour ECR repository "my_docker_repo" that we created previously
        ecr_repo = aws_ecr.Repository.from_repository_name(
            self, "MyEcrRepo", "my_docker_repo"
        )

        # Add a container to run in each task using our ECR image
        container = task_definition.add_container(
            "Container",
            image=aws_ecs.ContainerImage.from_ecr_repository(ecr_repo, tag="latest"),  # take "latest" Docker image
            logging=aws_ecs.LogDrivers.aws_logs(stream_prefix="ecs"), # easiest setup to view service logs in AWS
            health_check=aws_ecs.HealthCheck( # verify service health
                command=["CMD-SHELL", "curl -f http://localhost:80/ || exit 1"],
                interval=Duration.seconds(30),  # Check every 30 sec
                timeout=Duration.seconds(5),  # Fail if no response in 5 sec
                retries=3,  # Mark unhealthy after 3 failures
                start_period=Duration.seconds(10)  # Grace period after startup
            )
        )

        # Expose container port 80 (http)
        container.add_port_mappings(
            aws_ecs.PortMapping(container_port=80)
        )

        # Create a Fargate Service with 2 tasks, so we have 1 in each AZ
        # Actually, it's better to have 4 (2 per AZ) in case 1 AZ goes down, and we want remaining AZ to be resilient to task failures
        # But in this tutorial I proceed with 2 tasks.
        #
        # Our tasks are allocated in private subnet by default, check vpc_subnets= param in documentation
        service = aws_ecs.FargateService(
            self, "FargateService",
            cluster=cluster,
            task_definition=task_definition,
            desired_count=2
        )

        # Create an Application Load Balancer (ALB)
        # It will uniformly distribute incoming requests to our 2 tasks.
        # We use inter
        # What is ALB: https://docs.aws.amazon.com/elasticloadbalancing/latest/application/introduction.html
        alb = aws_elasticloadbalancingv2.ApplicationLoadBalancer(
            self, "Alb",
            vpc=vpc,
            internet_facing=True
        )

        # NOTE: if you don't have a domain yet, comment everything below: hosted_zone, alb_certificate and aws_route53.ARecord statements

        # Lookup a hosted zone attached to our domain
        # Hosted zone is a container for DNS records for our domain: https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/hosted-zones-working-with.html
        hosted_zone = aws_route53.HostedZone.from_lookup(self, "HostedZone", domain_name=DOMAIN)

        # Create an ACM certificate in order for internal domain to support HTTPS
        full_int_name = f"{INTERNAL_SUBDOMAIN}.{DOMAIN}"  # api-int.YOUR_DOMAIN_NAME
        alb_certificate = aws_certificatemanager.DnsValidatedCertificate(
            self, "Certificate",
            domain_name=full_int_name,
            hosted_zone=hosted_zone,
        )

        # Add DNS record to send all https://api-int.YOUR_DOMAIN_NAME requests to our API service
        # More about DNS records in general: https://www.cloudflare.com/learning/dns/dns-records/
        aws_route53.ARecord(
            self, "APIAliasRecord",
            zone=hosted_zone,
            record_name=INTERNAL_SUBDOMAIN,
            target=aws_route53.RecordTarget.from_alias(aws_route53_targets.LoadBalancerTarget(alb))
        )

        # Add a listener for the ALB on port 80 (http) and 443 (https)
        # Now ALB can accept input requests
        listener_http = alb.add_listener(
            "HttpListener",
            port=80,
            open=True
        )

        listener_https = alb.add_listener(
            "HttpsListener",
            port=443,
            open=True,
            certificates=[alb_certificate],
        )

        # Register the Fargate service as a target for ALB
        # Now ALB will send incoming requests to this target
        for listener in [listener_http, listener_https]:
            listener.add_targets(
                "EcsTargets",
                port=80,
                targets=[service.load_balancer_target(
                    container_name="Container",
                    container_port=80
                )],
                health_check=aws_elasticloadbalancingv2.HealthCheck(
                    path="/",  # should return 200 Ok
                    interval=Duration.seconds(30),  # same as task health check
                    timeout=Duration.seconds(5),
                    unhealthy_threshold_count=2,
                    healthy_threshold_count=2,
                )
            )


class CloudfrontStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Once again lookup a hosted zone attached to our domain
        hosted_zone = aws_route53.HostedZone.from_lookup(
            self, "HostedZone",
            domain_name=DOMAIN
        )

        full_ext_name = f"{EXTERNAL_SUBDOMAIN}.{DOMAIN}" # api.YOUR_DOMAIN_NAME
        full_int_name = f"{INTERNAL_SUBDOMAIN}.{DOMAIN}" # api-int.YOUR_DOMAIN_NAME

        # Create an ACM certificate in order for external domain to support HTTPS
        certificate = aws_certificatemanager.DnsValidatedCertificate(
            self, "Certificate",
            domain_name=full_ext_name,
            hosted_zone=hosted_zone,
        )

        # Create a CloudFront distribution accessible on external domain. It will reroute request to internal domain:
        # https://aws.amazon.com/blogs/networking-and-content-delivery/latency-based-routing-leveraging-amazon-cloudfront-for-a-multi-region-active-active-architecture/
        #
        # Cloudfront provides hundreds of Points of Presence all over the world, supports caching etc.
        # therefore improving performance.
        cloudfront_distribution = aws_cloudfront.Distribution(
            self, "CloudFrontDistribution",
            default_behavior=aws_cloudfront.BehaviorOptions(
                allowed_methods=aws_cloudfront.AllowedMethods.ALLOW_ALL, # we need all methods for API
                cache_policy=aws_cloudfront.CachePolicy.CACHING_DISABLED, # the most dummy approach
                origin_request_policy=aws_cloudfront.OriginRequestPolicy.ALL_VIEWER, # pass everything (headers, query params)
                response_headers_policy=aws_cloudfront.ResponseHeadersPolicy(self, "CORS", cors_behavior=aws_cloudfront.ResponseHeadersCorsBehavior(
                    access_control_allow_credentials=False,
                    access_control_allow_headers=["*"],
                    access_control_allow_methods=["ALL"],
                    access_control_allow_origins=[f"https://{DOMAIN}", f"https://www.{DOMAIN}"],
                    access_control_expose_headers=["*"],
                    access_control_max_age=Duration.seconds(60*10),
                    origin_override=True
                )),
                origin=aws_cloudfront_origins.HttpOrigin(
                    full_int_name,
                    protocol_policy=aws_cloudfront.OriginProtocolPolicy.HTTPS_ONLY
                ),
                viewer_protocol_policy=aws_cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS
            ),
            domain_names=[full_ext_name],
            certificate=certificate
        )

        # Send all https://api.YOUR_DOMAIN_NAME requests to Cloudfront
        aws_route53.ARecord(
            self, "ApiRecord",
            zone=hosted_zone,
            record_name=EXTERNAL_SUBDOMAIN,
            target=aws_route53.RecordTarget.from_alias(
                aws_route53_targets.CloudFrontTarget(cloudfront_distribution)
            )
        )
