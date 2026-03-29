# backend/Dockerfile
FROM python:3.11-slim
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir --upgrade -r ./requirements.txt
COPY src/ ./src/
EXPOSE 3001
CMD ["python", "./src/server.py"]