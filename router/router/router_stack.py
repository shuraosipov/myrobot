from aws_cdk import (
    Duration,
    Stack,
    aws_lambda as _lambda,
    aws_apigateway as api_gw,
    aws_iam as iam,
    # aws_sqs as sqs,
)
from constructs import Construct


class RouterStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        router_function_role = iam.Role(
            self,
            "lex_router_function_role",
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name(
                    "service-role/AWSLambdaBasicExecutionRole"
                ),
            ],
        )

        router_function_role.add_to_policy(
            iam.PolicyStatement(
                effect=iam.Effect.ALLOW,
                actions=["lambda:InvokeFunction"],
                resources=["*"],
            )
        )

        # create router function for lex fulfillment
        router_function = _lambda.Function(
            self,
            "lex-router-function",
            description="Typewriter AI Router for Telegram. Used to fulfill Lex intents.",
            runtime=_lambda.Runtime.PYTHON_3_9,
            handler="lambda_function.lambda_handler",
            code=_lambda.Code.from_asset("lambda"),
            role=router_function_role,
            timeout=Duration.seconds(15),
            environment={
                "create_article_intent": "typewriter_fulfullment_function",
            }
        )

        ### OUTPUTS ###
        self.router_function_name = router_function.function_name
