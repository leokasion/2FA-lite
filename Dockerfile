# Use the smallest viable Python image
FROM python:3.11-alpine

# Install only sys libs required for qrcode
RUN apk add --no-cache jpeg-dev zlib-dev libjpeg-turbo-dev gcc musl-dev curl

WORKDIR /app

# Install Python requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy only needed src code
COPY app.py .

# Security: run as a non privileged user
RUN adduser -D appuser && chown -R appuser /app
USER appuser

EXPOSE 5000

CMD ["python", "app.py"]