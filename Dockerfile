
# TODO: For local dev, execute docker login v-its-ciap-docker.repository.ucsd.edu and enter your UCSD AD username and AD password when prompted 
FROM r-its-python-docker.repository.ucsd.edu/3.11/rhel9.x/webapp:latest

RUN microdnf install -y tar
RUN microdnf install -y gzip
# Required dependency for Psycopg2
RUN microdnf install -y libpq-devel


# https://fastapi.tiangolo.com/deployment/docker/
# we first copy the file with the dependencies alone, not the rest of the code

# RUN pip install --only-binary :all: greenlet

COPY ./requirements.txt ./.env* /code/

# Mount secrets and install dependencies from artifactory and pypi
RUN --mount=type=secret,id=artifactory-user,required=true \
--mount=type=secret,id=artifactory-secret,required=true \
--mount=type=secret,id=artifactory-index,required=true \
pip3 install \
-r /code/requirements.txt \
--no-cache-dir \
--upgrade \
--index-url https://$(cat /run/secrets/artifactory-user):$(cat /run/secrets/artifactory-secret)@$(cat /run/secrets/artifactory-index) \
--extra-index-url https://pypi.org/simple

# copy all the code. As this is what changes most frequently, we put it near the end, because almost always, anything after this step will not be able to use the cache.
COPY ./app /code/app

# TODO: Probably remove this once a better local dev setup is worked out
EXPOSE 8080

# add option --proxy-headers if contaier behind load balancer like nginx
# USE THIS TOP CMD FOR WHEN YOU COMMIT SO THAT DEV/PROD WORKS
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080", "--proxy-headers", "--forwarded-allow-ips", "*"]

# USE THIS CMD FOR LOCAL DEVELOPMENT
#CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080", "--proxy-headers", "--forwarded-allow-ips", "*", "--ssl-keyfile=./app/config/local-key.pem", "--ssl-certfile=./app/config/local-cert.pem"]