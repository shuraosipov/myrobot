FROM ubuntu:22.04

COPY requirements.txt /workspace/
WORKDIR /workspace

RUN apt-get update && apt-get install -y python3 python3-pip ffmpeg
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

COPY bot /workspace/bot
WORKDIR /workspace/bot
CMD ["python3","-u", "app.py"]