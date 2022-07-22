# syntax=docker/dockerfile:1

FROM python

RUN apt-get update \
	&& apt-get install -y --no-install-recommends \
		sqlite3 \
	&& rm -rf /var/lib/apt/lists/*

WORKDIR /user/src/app

RUN pip install Django
RUN pip install djangorestframework
RUN pip install djoser
RUN pip install django-rest-swagger

ENV PYTHONUNBUFFERED=1

COPY ./instagtest .
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000", "-v", "3"]