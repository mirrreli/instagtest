# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster
WORKDIR /app

COPY . .

CMD [ "python3", "-m" , "python", "run", "--host=0.0.0.0"]