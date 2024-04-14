FROM python:3.9-slim
RUN apt-get update && apt-get install -y nginx iputils-ping && rm -rf /var/lib/apt/lists/*
ADD /app /app
RUN pip install Flask gunicorn bcrypt
WORKDIR /app
CMD ["python3", "app.py"]


