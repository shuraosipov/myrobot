import aws_cdk as core
import aws_cdk.assertions as assertions

from typewrtier.typewrtier_stack import TypewrtierStack

# example tests. To run these tests, uncomment this file along with the example
# resource in typewrtier/typewrtier_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = TypewrtierStack(app, "typewrtier")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
