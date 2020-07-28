FROM python:3.8
LABEL maintainer "INB Elixir"
RUN mkdir /service
RUN mkdir /service/registry
WORKDIR /service
COPY ./Network/api/registry /service/registry
COPY requirements.txt /service/requirements.txt
COPY init_registry_docker.sh /service/init.sh
RUN pip install -r requirements.txt

# Making testing files for the docker network.
RUN touch /service/registry/services.ini
RUN touch /service/registry/networks.ini
RUN echo "[beacon-net1]\nname = beacon-net1\ndescription = Testing network for the Beacon Network deployment.\norganization = INB" > /service/registry/networks.ini
RUN echo "[b1.bn.com]\nname = b1.bn.com\nserviceURL = http://b1.bn.com:5001\nopen = True\nentryPoint = False\nnetwork = beacon-net1\nServiceType = GA4GHBeacon" > /service/registry/services.ini
RUN echo "[b2.bn.com]\nname = b2.bn.com\nserviceURL = http://b2.bn.com:5002\nopen = True\nentryPoint = False\nnetwork = beacon-net1\nServiceType = GA4GHBeacon" >> /service/registry/services.ini
RUN echo "[b3.bn.com]\nname = b3.bn.com\nserviceURL = http://b3.bn.com:5003\nopen = True\nentryPoint = False\nnetwork = beacon-net1\nServiceType = GA4GHBeacon" >> /service/registry/services.ini
RUN echo "[ba1.bn.com]\nname = ba1.bn.com\nserviceURL = http://ba1.bn.com:5004\nopen = True\nentryPoint = False\nnetwork = beacon-net1\nServiceType = GA4GHBeaconAggregator" >> /service/registry/services.ini
