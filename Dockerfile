FROM python:3.8-slim-buster

LABEL authors="anchitdhar"

WORKDIR /code

RUN python -m pip install --upgrade pip

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . /code/

EXPOSE 8000

CMD ["flask", "--app", "app" ,"run", "--host=0.0.0.0", "--port=8000", "--debug"]
