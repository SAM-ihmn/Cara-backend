# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libpq-dev gcc g++ --no-install-recommends && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt ./

# Build arguments to differentiate between build and production
ARG MODE=build

# Install Python dependencies
RUN if [ "$MODE" = "build" ]; then pip install --no-cache-dir -r requirements.txt; fi

# Copy the current directory contents into the container at /app
COPY . .

# Install django-cors-headers
RUN pip install django-cors-headers

# Expose the port the app runs on
EXPOSE 8000

# Run the command to start Django's development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
