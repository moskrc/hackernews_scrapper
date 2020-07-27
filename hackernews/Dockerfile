# base image
FROM python:3.6.0

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/app

ENV PYTHONPATH=${PYTHONPATH}:${PWD}
RUN pip3 install poetry
RUN poetry config virtualenvs.create false

COPY pyproject.toml /usr/src/app

RUN poetry install --no-dev

COPY . /usr/src/app

RUN python3 manage.py recreate_db && python3 manage.py setup_dev && python3 manage.py fetch_fresh_data
