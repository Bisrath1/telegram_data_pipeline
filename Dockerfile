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
