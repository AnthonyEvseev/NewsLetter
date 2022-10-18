FROM python

WORKDIR /app

COPY . .

ADD main.py .

RUN pip3 install --upgrade pip

RUN pip3 install -r requirements.txt

RUN celery -A main.celery flower

RUN celery -A main.celery worker -l INFO

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

