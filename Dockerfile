# Use a lightweight base image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy your app files
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Use environment variables for host/port
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV=production

# Default port used by Flask
EXPOSE 5000

# Start the Flask app
CMD ["flask", "run"]
