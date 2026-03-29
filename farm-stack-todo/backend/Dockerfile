# Use Python slim image
FROM python:3.11-slim

# Set working directory inside container
WORKDIR /app

# Copy requirements and install
COPY requirements.txt ./
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy source code
COPY src/ ./src/

# Expose port
EXPOSE 3001

# Start server
CMD ["python", "./src/server.py"]