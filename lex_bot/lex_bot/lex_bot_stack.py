from aws_cdk import (
    # Duration,
    CfnOutput,
    Fn,
    CfnTag,
    Stack,
    # aws_sqs as sqs,
    aws_lex as lex,
    aws_iam as iam,
)
from constructs import Construct


class LexBotStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # ger variables from context
        fulfillment_lambda_arn = self.node.try_get_context("fulfillment_lambda_arn")
        aws_account_id = self.node.try_get_context("aws_account_id")
        bot_name = self.node.try_get_context("bot_name")

        # create service linked role for lex
        lex_service_linked_role = iam.CfnServiceLinkedRole(
            self,
            "lex_service_linked_role",
            aws_service_name="lexv2.amazonaws.com",
            custom_suffix=bot_name,
        )

        # role for lex bot
        lex_bot_role = iam.Role(
            self,
            "lex_bot_role",
            assumed_by=iam.ServicePrincipal("lexv2.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name("AmazonLexFullAccess"),
            ],
        )

        lex_bot_role.add_to_policy(
            iam.PolicyStatement(
                effect=iam.Effect.ALLOW,
                actions=["lambda:InvokeFunction"],
                resources=["*"],
            )
        )

        # create intent
        create_article_intent = lex.CfnBot.IntentProperty(
            name="create_article_intent",
            description="Intent for MyRobot app to create an article",
            sample_utterances=[
                lex.CfnBot.SampleUtteranceProperty(utterance="call my lambda"),
                lex.CfnBot.SampleUtteranceProperty(utterance="create an article"),
                lex.CfnBot.SampleUtteranceProperty(utterance="create article"),
                lex.CfnBot.SampleUtteranceProperty(utterance="generate new article"),
            ],
            fulfillment_code_hook=lex.CfnBot.FulfillmentCodeHookSettingProperty(
                enabled=True,
            ),
            dialog_code_hook=lex.CfnBot.DialogCodeHookSettingProperty(enabled=False),
            slots=[
                lex.CfnBot.SlotProperty(
                    name="title",
                    slot_type_name="AMAZON.FreeFormInput",
                    value_elicitation_setting=lex.CfnBot.SlotValueElicitationSettingProperty(
                        slot_constraint="Required",
                        prompt_specification=lex.CfnBot.PromptSpecificationProperty(
                            max_retries=2,
                            message_groups_list=[
                                lex.CfnBot.MessageGroupProperty(
                                    message=lex.CfnBot.MessageProperty(
                                        plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                            value="What is the title of the article?"
                                        ),
                                    )
                                )
                            ],
                        ),
                    ),
                ),
            ],
            slot_priorities=[
                lex.CfnBot.SlotPriorityProperty(slot_name="title", priority=1)
            ],
        )

        # fallback intent
        fallback_intent = lex.CfnBot.IntentProperty(
            name="FallbackIntent",
            description="Intent for MyRobot app to handle fallback",
            parent_intent_signature="AMAZON.FallbackIntent",
        )

        lex_bot_locale = lex.CfnBot.BotLocaleProperty(
            locale_id="en_US",
            nlu_confidence_threshold=0.3,
            intents=[create_article_intent, fallback_intent],
        )

        # create bot
        lex_bot = lex.CfnBot(
            self,
            "lex_bot",
            name="myrobot",
            description="Conversational bot for MyRobot app",
            # role_arn=lex_bot_role.role_arn,
            role_arn=f"arn:aws:iam::{aws_account_id}:role/aws-service-role/lexv2.amazonaws.com/AWSServiceRoleForLexV2Bots_{bot_name}",
            data_privacy={
                "ChildDirected": "False",
            },
            idle_session_ttl_in_seconds=300,
            bot_locales=[lex_bot_locale],
            bot_tags=[CfnTag(key="AppName", value="MyRobot")],
        )

        bot_id = Fn.get_att(lex_bot.logical_id, "Id").to_string()

        bot_version = lex.CfnBotVersion(
            self,
            "bot_version",
            bot_id=bot_id,
            bot_version_locale_specification=[
                lex.CfnBotVersion.BotVersionLocaleSpecificationProperty(
                    bot_version_locale_details=lex.CfnBotVersion.BotVersionLocaleDetailsProperty(
                        source_bot_version="DRAFT"
                    ),
                    locale_id="en_US",
                )
            ],
        )

        bot_alias = lex.CfnBotAlias(
            self,
            "bot_alias",
            bot_alias_name="dev",
            bot_id=bot_id,
            bot_version=bot_version.attr_bot_version,
            bot_alias_locale_settings=[
                lex.CfnBotAlias.BotAliasLocaleSettingsItemProperty(
                    locale_id="en_US",
                    bot_alias_locale_setting=lex.CfnBotAlias.BotAliasLocaleSettingsProperty(
                        enabled=True,
                        # the properties below are optional
                        code_hook_specification=lex.CfnBotAlias.CodeHookSpecificationProperty(
                            lambda_code_hook=lex.CfnBotAlias.LambdaCodeHookProperty(
                                code_hook_interface_version="1.0",
                                lambda_arn=fulfillment_lambda_arn,
                            )
                        ),
                    ),
                )
            ],
        )

        # Outputs
        
        bot_id_output = CfnOutput(self, "bot_id_output", value=bot_id)
        
        bot_version_output = CfnOutput(
            self, "bot_version_output", value=bot_version.attr_bot_version
        )
        bot_alias_id_output = CfnOutput(
            self, "bot_alias_id_output", value=bot_alias.attr_bot_alias_id
        )