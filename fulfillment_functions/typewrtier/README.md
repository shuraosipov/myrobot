## About
This is a fulfillment function for AWS Lex intent.
It is used to generate a response to the user based on the intent name and the slots provided by the user.

## Prerequisites
This function uses OpenAI package.
You need to create a Lambda Layer with OpenAI Python library using this [instructions](../../lambda_layer_builder/README.md) and update `cdk.context.json` with the Layer ARN.

Also, you need to have an OpenAI API key and save this key to AWS Secrets Manager in plaintext using `OPENAI_API_KEY` as its name.

## Install dependencies
```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt -t .
```

## Deploy
```
cdk synth
cdk deploy
```

## Test
```
bash tests/test_local.sh
```

## Useful commands

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation

Enjoy!
