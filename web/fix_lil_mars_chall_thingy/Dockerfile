FROM debian

WORKDIR /app

RUN apt update -y; apt install curl python3 python3-pip apt-utils -y
RUN apt install docker.io -y
#RUN curl -fsSL https://get.docker.com -o get-docker.sh; sh ./get-docker.sh --dry-run
RUN pip install --no-cache-dir flask --break-system-packages

COPY . .

CMD ["python3", "app.py"]

