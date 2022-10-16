FROM python:3.10-alpine

RUN adduser -D 1001

USER 0

WORKDIR /data/app

COPY --chown=1001:1001 ./project .

# hadolint ignore=DL3018
RUN apk add --no-cache --virtual .build-deps gcc libressl-dev musl-dev libffi-dev\
    && pip3 install --no-cache-dir -r requirements.txt \
    && apk del .build-deps libressl-dev musl-dev libffi-dev gcc

USER 1001

CMD ["sh", "-c", "python3 main.py"]