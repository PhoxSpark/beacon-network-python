FROM python:3.8
LABEL maintainer "INB Elixir"
RUN mkdir /service
RUN mkdir /service/view
WORKDIR /service
COPY ./Network/view /service/view
COPY requirements.txt /service/requirements.txt
RUN pip install -r requirements.txt