FROM selenium/standalone-chrome:latest

USER root

# Install Python and dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first (for better Docker caching)
COPY requirements.txt .

# Install Python packages
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy all application files
COPY . .

# Expose port for Flask app
EXPOSE 8080

# Set environment variables
ENV PYTHONUNBUFFERED=1
# Add your non-sensitive environment variables here
# ENV FLASK_ENV=production
# ENV LOG_LEVEL=info

# Run Flask app with gunicorn using application factory
# Increased timeout to 10 minutes, graceful timeout for Chrome cleanup
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--timeout", "600", "--graceful-timeout", "120", "--workers", "1", "--threads", "1", "web_app:create_app()"]