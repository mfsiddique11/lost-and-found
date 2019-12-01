from python:3.6.8

WORKDIR /app

COPY . /app

RUN pip3 install -r requirements.txt

ENTRYPOINT [python3]

CMD [run.py]
