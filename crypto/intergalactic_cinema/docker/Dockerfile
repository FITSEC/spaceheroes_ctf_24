FROM python:3.9-slim
RUN apt-get update && apt-get install -y nginx iputils-ping && rm -rf /var/lib/apt/lists/*
ADD /app /app
RUN pip install Flask gunicorn bcrypt
COPY nginx.conf /etc/nginx/sites-available/default
EXPOSE 80
CMD service nginx start && gunicorn --chdir /app app:app -b 0.0.0.0:5000
