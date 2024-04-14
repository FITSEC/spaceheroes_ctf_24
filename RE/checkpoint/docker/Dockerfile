
FROM ubuntu:23.10

RUN apt-get -y update && apt-get -y install xinetd python3

COPY checkpoint.py /
COPY flag.txt /	 
COPY service.conf /service.conf
COPY wrapper /wrapper
COPY banner_fail /banner_fail

RUN chmod 755 /checkpoint.py /wrapper
RUN chmod 744 /flag.txt

EXPOSE 31337

CMD ["/usr/sbin/xinetd", "-filelog", "-", "-dontfork", "-f", "/service.conf"]
