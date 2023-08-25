FROM python:3.8-slim-buster

LABEL authors="anchitdhar"

WORKDIR /app

RUN python -m pip install --upgrade pip

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD ["flask", "run", "app", "--debug"]