## About
This is a simple Telegram bot that can be hosted on a server. It is written in Python and uses the [python-telegram-bot]

## Test locally
```
docker build --platform=linux/amd64 -t telegram_bot . && docker run --env-file env.list telegram_bot
```

## Build and Push to ECR
Retrieve an authentication token and authenticate your Docker client to your registry:
```
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 419091122511.dkr.ecr.us-east-1.amazonaws.com
```

Build your Docker image using the following command:
```
docker build --platform=linux/amd64 -t telegram_bot .
```

Tag your image so you can push the image to this repository
```
docker tag telegram_bot:latest 419091122511.dkr.ecr.us-east-1.amazonaws.com/telegram_bot:latest
```

Push this image to your newly created AWS repository:
```
docker push 419091122511.dkr.ecr.us-east-1.amazonaws.com/telegram_bot:latest
```





