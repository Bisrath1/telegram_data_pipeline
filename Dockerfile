FROM python:3.10-slim

WORKDIR /app

# Copy dependency files
COPY vendor/ /vendor/
COPY requirements.txt requirements.txt

# First try local wheels, then fallback to PyPI
RUN pip install --no-cache-dir --find-links=/vendor/ -r requirements.txt || \
    pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

CMD ["bash"]

FROM python:3.10-slim

WORKDIR /app

COPY vendor/ /vendor/
RUN pip install --no-index --find-links=/vendor/ -r requirements.txt


COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
