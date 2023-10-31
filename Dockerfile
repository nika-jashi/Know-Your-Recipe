FROM python:3.10.11-slim-buster
LABEL maintener="nikajashi"

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /tmp/requirements.txt
COPY . /app
WORKDIR /app
EXPOSE 8000

RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    rm -rf /tmp && \
    adduser \
    --dissabled-password \
    --no-create-home \
    django-user

ENV PATH="/py/bin$PATH"

USER django-user

ENTRYPOINT ["sh","scripts/docker-entrypoint.sh"]