FROM python:3.10-slim

WORKDIR /app

COPY vendor/ /vendor/
RUN pip install --no-index --find-links=/vendor/ -r requirements.txt


COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
