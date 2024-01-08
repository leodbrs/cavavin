# Use an official Python runtime as a parent image
FROM python:3.12.0-slim

# Set the working directory to /app
WORKDIR /app

# Install system dependencies
RUN apt update && \
    apt install -y default-libmysqlclient-dev build-essential pkg-config

# Copy only the necessary files
COPY app app
COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

# Copy the entrypoint script to the image
COPY entrypoint.sh /usr/local/bin/

# Make the entrypoint script executable
RUN chmod +x /usr/local/bin/entrypoint.sh

EXPOSE 80
ENTRYPOINT ["entrypoint.sh"]

# Run Gunicorn as the WSGI server
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:80", "app:app"]
