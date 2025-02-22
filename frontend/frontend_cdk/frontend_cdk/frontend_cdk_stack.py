from aws_cdk import (
    Stack,
    aws_route53,
    aws_route53_targets,
    aws_certificatemanager,
    aws_cloudfront,
    aws_cloudfront_origins,
    aws_s3 as s3,
    aws_iam as iam,
)
from constructs import Construct

DOMAIN = "YOUR_DOMAIN"
BUCKET_NAME = "YOUR_DESIRED_BUCKET_NAME"


class FrontendCdkStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Lookup a hosted zone attached to our domain
        hosted_zone = aws_route53.HostedZone.from_lookup(
            self, "HostedZone", domain_name=DOMAIN
        )

        www_domain = f"www.{DOMAIN}"
        # Create an ACM certificate in order for website domain to support HTTPS
        certificate = aws_certificatemanager.DnsValidatedCertificate(
            self,
            "Certificate",
            domain_name=DOMAIN,
            hosted_zone=hosted_zone,
            subject_alternative_names=[www_domain],
        )

        website_bucket = s3.Bucket(self, "S3Bucket", bucket_name=BUCKET_NAME)

        # allow cloudfront to access bucket objects
        oac = aws_cloudfront.S3OriginAccessControl(
            self,
            "OAC",
        )

        behavior_without_cache = aws_cloudfront.BehaviorOptions(
            origin=aws_cloudfront_origins.S3BucketOrigin(
                website_bucket, origin_access_control_id=oac.origin_access_control_id
            ),
            viewer_protocol_policy=aws_cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
            allowed_methods=aws_cloudfront.AllowedMethods.ALLOW_GET_HEAD,
            cache_policy=aws_cloudfront.CachePolicy.CACHING_DISABLED,
        )
        behavior_with_cache = aws_cloudfront.BehaviorOptions(
            origin=aws_cloudfront_origins.S3BucketOrigin(
                website_bucket, origin_access_control_id=oac.origin_access_control_id
            ),
            viewer_protocol_policy=aws_cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
            allowed_methods=aws_cloudfront.AllowedMethods.ALLOW_GET_HEAD,
        )
        distribution = aws_cloudfront.Distribution(
            self,
            "WebsiteDistribution",
            default_behavior=behavior_without_cache,
            additional_behaviors={
                "/favicon.ico": behavior_with_cache,
                "/assets/*": behavior_with_cache,
            },
            default_root_object="index.html",
            domain_names=[DOMAIN, www_domain],
            certificate=certificate,
        )
        website_bucket.add_to_resource_policy(
            iam.PolicyStatement(
                actions=["s3:GetObject"],
                resources=[website_bucket.arn_for_objects("*")],
                principals=[iam.ServicePrincipal("cloudfront.amazonaws.com")],
                conditions={
                    "StringEquals": {"AWS:SourceArn": distribution.distribution_arn}
                },
            )
        )

        aws_route53.ARecord(
            self,
            "AliasRecord",
            zone=hosted_zone,
            record_name=DOMAIN,
            target=aws_route53.RecordTarget.from_alias(
                aws_route53_targets.CloudFrontTarget(distribution)
            ),
        )

        # Optionally, add a record for www subdomain (if using one)
        aws_route53.ARecord(
            self,
            "AliasRecordWWW",
            zone=hosted_zone,
            record_name=www_domain,
            target=aws_route53.RecordTarget.from_alias(
                aws_route53_targets.CloudFrontTarget(distribution)
            ),
        )
