FROM python:3.12-slim-bullseye

WORKDIR /app

COPY requirements.txt .
COPY requirements-dev.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

#CMD ["python", "node_api.py"] 
CMD redis-server --daemonize yes && python node_api.py