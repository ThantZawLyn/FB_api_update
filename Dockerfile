FROM tiangolo/uwsgi-nginx-flask:python3.8

WORKDIR /pysetup
COPY ./app/requirements.txt /pysetup/

RUN mkdir /app/screenshots
RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /app

COPY ./app/ /app/
