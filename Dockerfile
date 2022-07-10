FROM python:3.10-buster
ARG requirements=requirements.txt
COPY $requirements $requirements
RUN pip install --no-cache-dir --upgrade -r $requirements
COPY . /app
WORKDIR /app

EXPOSE 8000
# Use heroku entrypoint
CMD ["bash", "local_dev.sh"]
