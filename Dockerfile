# TODO: For local dev, execute docker login repository.ucsd.edu and enter your UCSD email and AD password when prompted
FROM v-its-ciap-docker.repository.ucsd.edu/rhel/minimal/8.x/python/3.9/webapp:v19

RUN microdnf install tar
RUN microdnf install gzip

EXPOSE 8080

# https://fastapi.tiangolo.com/deployment/docker/
# we first copy the file with the dependencies alone, not the rest of the code
COPY ./requirements.txt ./.env* /code/


RUN python3.9 -m pip install --use-pep517 --no-cache-dir --upgrade -r /code/requirements.txt

# copy all the code. As this is what changes most frequently, we put it near the end, because almost always, anything after this step will not be able to use the cache.
COPY ./app /code/app

# add option --proxy-headers if contaier behind load balancer like nginx
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080", "--proxy-headers", "--forwarded-allow-ips", "*"]
#CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080", "--proxy-headers", "--forwarded-allow-ips", "*", "--ssl-keyfile=./app/config/local-key.pem", "--ssl-certfile=./app/config/local-cert.pem"]
