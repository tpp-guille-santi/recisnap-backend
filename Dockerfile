FROM python:3.9-slim as requirements-stage
WORKDIR /tmp
RUN pip install poetry
COPY ./pyproject.toml ./poetry.lock* /tmp/
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes
FROM python:3.9-slim
WORKDIR /app
COPY --from=requirements-stage /tmp/requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY ./app /app
COPY ./local_dev.sh /local_dev.sh

EXPOSE 8000
CMD ["bash", "local_dev.sh"]
