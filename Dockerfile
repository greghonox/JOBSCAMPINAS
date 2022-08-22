FROM python:3.8-slim

WORKDIR /app

COPY . .

RUN apt update; apt install -y python3 python3-dev python3-pip

RUN /usr/local/bin/python3 -m pip install --upgrade pip

RUN pip3 install -r /app/requirements.txt

CMD ["python", "/app/main.py", "-t", "15"]
