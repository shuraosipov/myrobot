import uuid

from aws_cdk import (
    Duration,
    Stack,
    aws_lambda as _lambda,
    aws_iam as iam,
    aws_secretsmanager as secrets_manager,
)
from constructs import Construct

class TypewrtierStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # get context parameters
        layer_version_arns = self.node.try_get_context("layer_version_arns")

        # get openai token from secrets manager
        openai_api_key = secrets_manager.Secret.from_secret_name_v2(
            self, "openai_api_key", secret_name="OPENAI_API_KEY"
        )

        # import lambda layer
        # a function that return list of layers based on layer version arn
        def get_layers(layer_version_arns):
            layers = []

            for layer_version in layer_version_arns:
                layer = _lambda.LayerVersion.from_layer_version_arn(
                    scope=self, 
                    id=f"layer_{uuid.uuid4().hex}", 
                    layer_version_arn=layer_version

                )
                layers.append(layer)
            return layers

        function = _lambda.Function(
            self,
            "fulfullment_function",
            function_name="typewriter_fulfullment_function",
            description="Typewriter AI function for my Robot. It uses OpenAI to generate text replies.",
            runtime=_lambda.Runtime.PYTHON_3_9,
            handler="lambda_function.lambda_handler",
            code=_lambda.Code.from_asset("lambda"),
            layers=get_layers(layer_version_arns),
            timeout=Duration.seconds(15),
            environment={
                "OPENAI_API_KEY": openai_api_key.secret_value.unsafe_unwrap(),
            },
        )

