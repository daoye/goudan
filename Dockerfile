FROM python:alpine3.7

LABEL Name=goudan Version=0.0.1
EXPOSE 1991

WORKDIR /app
ADD ./src /app

RUN apk add --no-cache gcc  --virtual .build-deps\
        && apk add --no-cache musl-dev libxslt-dev\
        && python3 -m pip install -r requirements.txt \
        && apk del .build-deps
ENTRYPOINT [ "python3", "main.py"]
