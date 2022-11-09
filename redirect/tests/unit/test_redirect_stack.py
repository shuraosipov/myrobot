import aws_cdk as core
import aws_cdk.assertions as assertions

from redirect.redirect_stack import RedirectStack

# example tests. To run these tests, uncomment this file along with the example
# resource in redirect/redirect_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = RedirectStack(app, "redirect")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
