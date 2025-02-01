#!/usr/bin/env python3
import os

import aws_cdk as cdk

from backend_cdk.backend_cdk_stack import ApiStack, CloudfrontStack


ACCOUNT_ID = "YOUR_ACCOUNT_ID"

app = cdk.App()
api_stack = ApiStack(app, "ApiStack",
        cross_region_references=True,
        env=cdk.Environment(
            account=ACCOUNT_ID,
            region="eu-west-1"
        )
    )

# NOTE: if you don't have a domain registered yet, comment cloudfront_stack
# You wil still have access to API through load balancer DNS name
cloudfront_stack = CloudfrontStack(app, "CloudfrontStack",
        cross_region_references=True,
        env=cdk.Environment(
            account=ACCOUNT_ID,
            # cloudfront is a global service. All actions with global services are performed in "us-east-1"
            region="us-east-1"
        )
    )

app.synth()
