FROM python:3.7-buster

LABEL Name=goudan Version=0.0.1
EXPOSE 1991 1992 1993 1994

WORKDIR /app
ADD ./src /app

RUN apt-get -y update && apt-get -y install gcc libxslt-dev masscan\
        && python3 -m pip install -r requirements.txt
ENTRYPOINT [ "python3", "main.py"]
