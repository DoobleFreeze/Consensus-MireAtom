FROM python:3.11

WORKDIR /opt/app

COPY app_web/configs/dev/requirements.txt .

RUN pip3 install -r /opt/app/requirements.txt

COPY ./app_web .

CMD gunicorn --bind 0.0.0.0:4009 manage:app --worker-class=gevent --timeout 300