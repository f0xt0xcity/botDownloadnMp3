FROM python:latest

WORKDIR /app

COPY .env ./

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY main.py ./

CMD python ./main.py 