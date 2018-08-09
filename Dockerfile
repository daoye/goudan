FROM python:alpine3.7

LABEL Name=goudan Version=0.0.1
EXPOSE 1991

WORKDIR /app
ADD ./src /app

RUN apk add --no-cache gcc musl-dev libxslt-dev  --virtual .build-deps\
        && python3 -m pip install -r requirements.txt \
        && apk del .build-deps
# CMD ["python3", "-m", "goudan"]
ENTRYPOINT [ "python3", "main.py"]
