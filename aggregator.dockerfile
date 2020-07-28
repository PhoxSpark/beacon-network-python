FROM python:3.8
LABEL maintainer "INB Elixir"
RUN mkdir /service
RUN mkdir /service/aggregator
WORKDIR /service
COPY ./Network/api/aggregator /service/aggregator
COPY requirements.txt /service/requirements.txt
RUN pip install -r requirements.txt

RUN touch /service/aggregator/services.ini

RUN echo "[r1.bn.com]\nname = r1.bn.com\nServiceType = GA4GHRegistry\nserviceURL = http://r1.bn.com:5005" > /service/aggregator/services.ini