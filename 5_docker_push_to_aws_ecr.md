# AWS cloud deploy - starting steps
Now it's time to deploy our backend app.
1) First, create [AWS account](https://aws.amazon.com/console/) and install [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html):

```shell
# You need to run smth like this:
curl "https://awscli.amazonaws.com/AWSCLIV2.pkg" -o "AWSCLIV2.pkg"
sudo installer -pkg AWSCLIV2.pkg -target /
```

2) Authorize yourself in [AWS CLI](https://docs.aws.amazon.com/cli/v1/userguide/cli-authentication-user.html)
  - In this tutorial we don't create IAM users, we do everything from the root user.
  - Therefore, you can use access keys from you root user [[docs]](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_root-user_manage_add-key.html)
2) We are going to use `eu-west-1` region as primary: 
```
# AWS CLI authorize questions:
...
Default region name [None]: eu-west-1
Default output format [None]: json
```

3) Next, create private ECR repository to upload our docker image there [[docs]](https://docs.aws.amazon.com/AmazonECR/latest/userguide/example_ecr_CreateRepository_section.html
):
```shell
aws ecr create-repository --repository-name my_docker_repo
```
4) Now, push our `myimage:latest` to ECR repo [[docs]](https://docs.aws.amazon.com/AmazonECR/latest/userguide/docker-push-ecr-image.html):

```
# use your <aws_account_id>
aws ecr get-login-password | docker login --username AWS --password-stdin <aws_account_id>.dkr.ecr.eu-west-1.amazonaws.com 
docker tag myimage:latest <aws_account_id>.dkr.ecr.eu-west-1.amazonaws.com/my_docker_repo:latest
docker push <aws_account_id>.dkr.ecr.eu-west-1.amazonaws.com/my_docker_repo:latest
```
5) In next step, we will setup the whole cloud infrastructure to host this backend image (our API server)