#!/usr/bin/env python3
import os

import aws_cdk as cdk

from frontend_cdk.frontend_cdk_stack import FrontendCdkStack


app = cdk.App()

ACCOUNT_ID = "ACCOUNT"

cloudfront_stack = FrontendCdkStack(app, "FrontendCdkStack",
        cross_region_references=True,
        env=cdk.Environment(
            account=ACCOUNT_ID,
            # cloudfront is a global service. All actions with global services are performed in "us-east-1"
            region="us-east-1"
        )
    )

app.synth()
