FROM python:3.6.8

WORKDIR /app

COPY . /app

RUN pip3 install -r requirements.txt

RUN chmod +x ./run_web.sh

