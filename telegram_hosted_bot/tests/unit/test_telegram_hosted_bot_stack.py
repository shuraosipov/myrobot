import aws_cdk as core
import aws_cdk.assertions as assertions

from telegram_hosted_bot.telegram_hosted_bot_stack import TelegramHostedBotStack

# example tests. To run these tests, uncomment this file along with the example
# resource in telegram_hosted_bot/telegram_hosted_bot_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = TelegramHostedBotStack(app, "telegram-hosted-bot")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
