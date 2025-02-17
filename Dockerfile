FROM python:3.13-slim

WORKDIR /app

RUN apt update \
  && apt install -y curl gcc git \
  && pip install --upgrade pip

COPY requirements.txt /requirements.txt

RUN pip install -r /requirements.txt

COPY . /app

CMD [ "python3", "search_paralax.py" ]
