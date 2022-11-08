from aws_cdk import (
    # Duration,
    Stack,
    aws_ecs as ecs,
    aws_ecr as ecr,
    aws_ec2 as ec2,
    aws_iam as iam,
    aws_secretsmanager as sm,
)
from constructs import Construct


class TelegramHostedBotStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        vpc = ec2.Vpc.from_lookup(self, "VPC", is_default=True)

        cluster = ecs.Cluster(
            self,
            "Cluster",
            cluster_name="telegram-hosted-bot-cluster",
            vpc=vpc,
        )

        ecr_repository = ecr.Repository.from_repository_name(
            self, "ECRRepository", "telegram_bot"
        )

        image = ecs.ContainerImage.from_ecr_repository(ecr_repository, tag="latest")

        task_definition = ecs.TaskDefinition(
            self,
            "telegram-hosted-bot-task-definition",
            compatibility=ecs.Compatibility.FARGATE,
            memory_mib="512",
            cpu="256",
        )

        telegram_token = sm.Secret.from_secret_name_v2(
            self, "telegram_token", secret_name="TELEGRAM_TOKEN"
        )

        task_definition.add_container(
            "telegram-hosted-bot-container",
            image=image,
            logging=ecs.LogDrivers.aws_logs(stream_prefix="telegram-hosted-bot"),
            secrets={"TELEGRAM_TOKEN": ecs.Secret.from_secrets_manager(telegram_token)},
        )

        task_execution_policy = iam.PolicyStatement(
            effect=iam.Effect.ALLOW,
            actions=[
                "logs:CreateLogStream",
                "logs:PutLogEvents",
                "logs:CreateLogGroup",
                "ecr:GetAuthorizationToken",
                "ecr:BatchCheckLayerAvailability",
                "ecr:GetDownloadUrlForLayer",
                "ecr:BatchGetImage",
                "lex:RecognizeText",
                "secretsmanager:GetSecretValue",
            ],
            resources=["*"],
        )

        task_definition.add_to_task_role_policy(task_execution_policy)

        default_sg = ec2.SecurityGroup.from_lookup_by_name(
            self, "DefaultSG", vpc=vpc, security_group_name="default"
        )

        # crate fargate service
        service = ecs.FargateService(
            self,
            "telegram-hosted-bot-service",
            cluster=cluster,
            task_definition=task_definition,
            desired_count=1,
            assign_public_ip=True,
            security_groups=[default_sg],
        )
