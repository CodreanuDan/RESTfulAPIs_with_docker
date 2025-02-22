
# Python base image
FROM python:3.11-slim

# Choose workdir
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variables from .env file
ENV WEATHER_API_KEY=${WEATHER_API_KEY}

# Expose port 8080 for the application to be available
EXPOSE 8080

# Run the application
CMD ["python", "main.py"]

