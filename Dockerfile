FROM tiangolo/uwsgi-nginx-flask:python3.6-alpine3.7

COPY ./app /app/app
COPY requirements.txt /app/

RUN pip install --upgrade pip && \
    pip3 install --trusted-host pypi.python.org -r /app/requirements.txt

COPY ./app/uwsgi.ini /app/