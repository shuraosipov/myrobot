## About
This CDK project is used to deploy Webhook (API Gateway + Lambda) for Telegram Bot. 

## Prerequisites
1) Fill in parameters in `cdk.context.json`.
2) Lambda layer with `requests` library. You can use `lambda-layer-requests` project to create it.
3) Secret in AWS Secrets Manager with Telegram Bot token. Secret name should be `TELEGRAM_TOKEN`.

## Install dependencies
```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt'

```

## Deploy
```
cdk synth
cdk deploy
```

## Useful commands

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation

Enjoy!
