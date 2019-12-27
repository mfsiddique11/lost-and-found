FROM python:3.6

WORKDIR /app

COPY . /app

RUN pip3 install -r requirements.txt

RUN chmod +x ./bin/run_web.sh

