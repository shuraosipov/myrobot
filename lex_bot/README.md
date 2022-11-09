## About
This CDK app deploys a Lex V2 bot. The bot is configured to use a Lambda function as a fulfillment code hook.

## Prerequisites
Update `cdk.context.json` with the following values:
- fulfillment_lambda_arn
- aws_account_id
- bot_name


## Install dependencies 

```
$ python3 -m venv .venv
$ source .venv/bin/activate
$ pip install -r requirements.txt
```

## Deploy

```
$ cdk synth
$ cdk deploy
```

## Useful commands

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation

Enjoy!
