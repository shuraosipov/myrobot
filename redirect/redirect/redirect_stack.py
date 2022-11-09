from aws_cdk import (
    # Duration,
    Stack,
    # aws_sqs as sqs,
    aws_apigateway as apigateway,
)
from constructs import Construct


class RedirectStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # get varibables from context
        integration_url = self.node.try_get_context("telegram_bot_url")
        app_name = self.node.try_get_context("app_name")

        # create api
        api = apigateway.RestApi(self, "redirect-api", rest_api_name=f"{app_name}-auth")

        # integration options for http api
        integration_options = apigateway.IntegrationOptions(
            integration_responses=[
                apigateway.IntegrationResponse(
                    status_code="200",
                )
            ],
            request_parameters={
                "integration.request.querystring.start": "'method.request.querystring.code'",
            },
            passthrough_behavior=apigateway.PassthroughBehavior.WHEN_NO_MATCH,
        )

        integration = apigateway.Integration(
            type=apigateway.IntegrationType.HTTP,
            integration_http_method="GET",
            uri=integration_url,
            options=integration_options,
        )

        api.root.add_method(
            "ANY",
            integration,
            method_responses=[
                apigateway.MethodResponse(
                    status_code="200",
                    response_models={"text/html": apigateway.Model.EMPTY_MODEL},
                ),
            ],
            request_parameters={
                "method.request.querystring.code": True,
            },
        )

        # create deployment
        deployment = apigateway.Deployment(self, "redirect-deployment", api=api)

        # create stage
        stage = apigateway.Stage(
            self, "redirect-stage", stage_name="redirect", deployment=deployment
        )
