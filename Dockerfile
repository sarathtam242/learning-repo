# Use an official Python base image
FROM python:3.13-slim

# Set the working directory inside the container
WORKDIR /app

# Copy dependency list first for better Docker layer caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code
COPY app/ ./app/

# Application listens on port 8080
EXPOSE 8080

# Start the FastAPI application using Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
