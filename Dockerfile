# Base image
FROM python:3.11-slim

# Set work directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy project
COPY . .

# Expose port
EXPOSE 8000

# Run server
CMD ["gunicorn", "gamereviews.wsgi:application", "--bind", "0.0.0.0:8000"]
