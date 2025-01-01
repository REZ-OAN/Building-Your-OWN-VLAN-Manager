# Use a Python base image
FROM python:3.9-slim

# Install necessary packages
RUN apt-get update && apt-get install -y \
    iproute2 \
    && apt-get clean

# Set the working directory
WORKDIR /app

# Copy the Flask app files
COPY app.py /app/
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose Flask app port
EXPOSE 5000

# Run the Flask app
CMD ["python", "app.py"]
