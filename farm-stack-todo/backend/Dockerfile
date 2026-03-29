FROM python:3.11-slim

WORKDIR /app

# Copy dependencies and install
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend source code
COPY src/ ./src/

EXPOSE 3001

CMD ["python", "./src/server.py"]