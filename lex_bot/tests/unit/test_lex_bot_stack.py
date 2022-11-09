import aws_cdk as core
import aws_cdk.assertions as assertions

from lex_bot.lex_bot_stack import LexBotStack

# example tests. To run these tests, uncomment this file along with the example
# resource in lex_bot/lex_bot_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = LexBotStack(app, "lex-bot")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
