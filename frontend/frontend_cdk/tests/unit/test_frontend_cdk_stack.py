import aws_cdk as core
import aws_cdk.assertions as assertions

from frontend_cdk.frontend_cdk_stack import FrontendCdkStack


# example tests. To run these tests, uncomment this file along with the example
# resource in frontend_cdk/frontend_cdk_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = FrontendCdkStack(app, "frontend-cdk")
    template = assertions.Template.from_stack(stack)


#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
