FROM python:3.10.11-slim-buster

LABEL maintainer="nikajashi"

ENV PYTHONUNBUFFERED 1

COPY requirements/requirements.txt /tmp/requirements.txt
COPY requirements/requirements.dev.txt /tmp/requirements.dev.txt
COPY . /app

WORKDIR /app
EXPOSE 8000

ARG DEV=false

RUN pip install --upgrade pip \
    && pip install -r /tmp/requirements.txt \
    && if [ "$DEV" = "true" ]; then pip install -r /tmp/requirements.dev.txt ; fi \
    && rm -rf /tmp

ENV PATH="/py/bin:$PATH"

USER root

RUN chmod +x /app/scripts/docker-entrypoint.sh

ENTRYPOINT ["/app/scripts/docker-entrypoint.sh"]
