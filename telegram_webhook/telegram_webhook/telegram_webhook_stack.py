from aws_cdk import (
    Duration,
    Environment,
    Stack,
    aws_lambda as _lambda,
    aws_apigateway as api_gw,
    aws_iam as iam,
    aws_secretsmanager as secrets_manager,
)
from constructs import Construct


class TelegramWebhookStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # get context parameters
        BOT_ID = self.node.try_get_context("LEX_BOT_ID")
        BOT_ALIAS_ID = self.node.try_get_context("LEX_BOT_ALIAS_ID")
        TELEGRAM_BASE_URL = self.node.try_get_context("TELEGRAM_BASE_URL")
        AWS_ACCOUNT_ID = self.node.try_get_context("AWS_ACCOUNT_ID")
        REGION = self.node.try_get_context("REGION")

        # get telegram token from secrets manager
        telegram_token = secrets_manager.Secret.from_secret_name_v2(
            self, "telegram_token", secret_name="TELEGRAM_TOKEN"
        )

        # iam role for lambda
        lambda_role = iam.Role(
            self,
            "lambda_role",
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name(
                    "service-role/AWSLambdaBasicExecutionRole"
                ),
            ],
        )

        lambda_role.add_to_policy(
            iam.PolicyStatement(
                effect=iam.Effect.ALLOW,
                actions=[
                    "lex:RecognizeText",
                ],
                resources=[
                    f"arn:aws:lex:{REGION}:{AWS_ACCOUNT_ID}:bot-alias/{BOT_ID}/{BOT_ALIAS_ID}"
                ],
            )
        )

        # import lambda layer
        layer = _lambda.LayerVersion.from_layer_version_arn(
            self,
            "layer",
            layer_version_arn=f"arn:aws:lambda:{REGION}:{AWS_ACCOUNT_ID}:layer:requests:1",
        )

        # webhook for telegram bot
        webhook_function = _lambda.Function(
            self,
            "webhook_function",
            description="Typewriter AI Webhook for Telegram. It handles the communication between Telegram and Lex.",
            runtime=_lambda.Runtime.PYTHON_3_9,
            handler="lambda_function.lambda_handler",
            code=_lambda.Code.from_asset("lambda"),
            role=lambda_role,
            layers=[layer],
            timeout=Duration.seconds(15),
            environment={
                "TELEGRAM_TOKEN": telegram_token.secret_value.unsafe_unwrap(),
                "TELEGRAM_BASE_URL": TELEGRAM_BASE_URL,
                "LEX_BOT_ID": BOT_ID,
                "LEX_BOT_ALIAS_ID": BOT_ALIAS_ID,
            },
        )

        # create api gateway
        api = api_gw.LambdaRestApi(
            self,
            "webhook_api_gw",
            handler=webhook_function,
            proxy=True,
        )
