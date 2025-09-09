# Use official Python image
FROM python:3.11-slim

# Avoid writing .pyc files
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Create working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy client code
COPY . .

# Default command: run your upload script
# You can override this in docker-compose or via `docker-compose run client python upload_file.py ...`
CMD ["python", "upload_file.py"]