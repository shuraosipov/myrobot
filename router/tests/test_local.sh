cdk synth --no-staging > template.yaml
sam local invoke lex-router-function --event tests/lex-to-lambda-event.json