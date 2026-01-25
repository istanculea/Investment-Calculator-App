# Use an official lightweight Python image as base
# Use a patched Python base image. Python ≥3.10.12
# We use Python 3.12 here to ensure PEP 706 support and long‑term
# maintenance stability.
FROM python:3.12-slim

RUN apt-get update && \
    apt-get install -y --no-install-recommends libarchive-tools && \
    rm -rf /var/lib/apt/lists/*

# Set the working directory inside the container
WORKDIR /app

# Copy dependency definitions first to leverage Docker cache
COPY requirements.txt ./

# Upgrade pip and wheel to patched versions before installing other
# dependencies.
RUN pip install --no-cache-dir --upgrade "pip>=23.3" && \
    pip install --no-cache-dir --upgrade "wheel>=0.46.2"

# Install Python dependencies listed in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code into the container
COPY . ./

# Expose the port the app listens on
EXPOSE 5000

# Run the Flask application
CMD ["python", "app.py"]