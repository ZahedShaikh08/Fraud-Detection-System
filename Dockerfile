# Use a slim Python base image
FROM python:3.10-slim

# Prevent creation of .pyc files and buffering issues
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Copy requirements first (leverages Docker cache)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install Gunicorn for serving the app
RUN pip install --no-cache-dir gunicorn

# Copy the rest of your code
COPY . .

# Expose the port Render uses
EXPOSE 10000

# Start the app via Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:10000", "api.app:app"]