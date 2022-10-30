cdk synth --no-staging > template.yaml
sam local invoke fulfullment_function --event tests/lex-to-lambda-event.json