FROM python:3.8
LABEL maintainer "INB Elixir"
RUN mkdir /service
RUN mkdir /service/beacon
WORKDIR /service
COPY ./Network/api/beacon /service/beacon
COPY requirements.txt /service/requirements.txt
RUN pip install -r requirements.txt

RUN touch /service/beacon/database.ini

RUN echo "[database]\nuser = microaccounts_dev\npassword = testpassword\nurl = db.bn.com\nport = 5432\ndatabase = elixir_beacon_dev" > /service/beacon/database.ini