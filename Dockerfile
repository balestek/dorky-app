FROM python:3.13-slim

WORKDIR /app

COPY . .

RUN apt-get update && apt-get upgrade -y && pip install --upgrade pip

RUN pip install .

EXPOSE 8080

ENTRYPOINT ["dorky-app", "start"]