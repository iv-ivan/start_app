# Deploy SPA to AWS
We will follow this [guide](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/getting-started-cloudfront-overview.html)

1) Create S3 bucket to store our static assets. Copy `BUCKET` name, we will use it later.
2) I've patch `input_field.tsx` to fetch API via `DOMAIN`, not localhost. But it's better to solve this by frontend dev/prod build configuration.
3) Upload static assets to S3:
```shell
# Use your BUCKET name
cd frontend/app
npm run build
aws s3 cp build/client/ s3://<BUCKET>/ --recursive
```
4) Init CDK:
```
mkdir frontend_cdk
cd frontend_cdk
cdk init app --language python
```

5) I've added `FrontendCdkStack` in `frontend_cdk_stack.py` and `app.py`. Don't forget to use your `DOMAIN`, `BUCKET` and `ACCOUNT_ID`
6) Deploy: `cdk deploy FrontendCdkStack`
7) Finally, we must add CORS headers to our backend API to allow requests from our `DOMAIN`, so that website can fetch API.
```python
# Edit backend_cdk_stack.py
...
# cloudfront section
response_headers_policy=aws_cloudfront.ResponseHeadersPolicy(self, "CORS", cors_behavior=aws_cloudfront.ResponseHeadersCorsBehavior(
    access_control_allow_credentials=False,
    access_control_allow_headers=["*"],
    access_control_allow_methods=["ALL"],
    access_control_allow_origins=[f"https://{DOMAIN}", f"https://www.{DOMAIN}"],
    access_control_expose_headers=["*"],
    access_control_max_age=Duration.seconds(60*10),
    origin_override=True
)),
```
```shell
cdk deploy CloudfrontStack
```
8) Now we can test it. Open your `https://{DOMAIN}` in browser:
<img width="865" alt="Screenshot 2025-02-22 at 21 09 40" src="https://github.com/user-attachments/assets/64413d7c-6641-4da8-a818-dbc5841db6ba" />
