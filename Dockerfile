FROM python:3.10.11-slim-buster

LABEL maintainer="nikajashi"

ENV PYTHONUNBUFFERED 1

COPY requirements/requirements.txt /tmp/requirements.txt
COPY requirements/requirements.dev.txt /tmp/requirements.dev.txt
COPY . /app

WORKDIR /app
EXPOSE 8000

ARG DEV=false

RUN python -m venv /py && /py/bin/pip install --upgrade pip && /py/bin/pip install -r /tmp/requirements.txt && if [ "$DEV" = "true" ]; then /py/bin/pip install -r /tmp/requirements.dev.txt ; fi && rm -rf /tmp

ENV PATH="/py/bin:$PATH"

USER root

ENTRYPOINT ["/app/scripts/docker-entrypoint.sh"]
