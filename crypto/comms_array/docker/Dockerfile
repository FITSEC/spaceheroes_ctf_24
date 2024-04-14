FROM alpine:latest

RUN apk add --no-cache bash socat python3
WORKDIR /app

COPY comms_array.py /app/comms_array.py
RUN chmod +x /app/comms_array.py

ENV FLAG="shctf{voyager_golden_record_transmission_1337}"
ENV PORT=1234

COPY start.sh /app/start.sh
RUN chmod +x /app/start.sh
EXPOSE 1234

CMD ["/app/start.sh"]

