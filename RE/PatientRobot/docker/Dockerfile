FROM ubuntu:latest

RUN apt-get -qq update && apt-get install -y make gcc -qq xinetd

copy chal/PatientRobot /chal
run chmod +x /chal  
copy flag/flag.txt /flag.txt
copy config/* /

run chmod 755 /chal

EXPOSE 32420/TCP

cmd ["/usr/sbin/xinetd", "-filelog", "-", "-dontfork", "-f", "/service.conf"]