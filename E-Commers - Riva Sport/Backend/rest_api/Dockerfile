FROM python:3

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . /app/

CMD ["python", "manage.prod.py", "migrate"]