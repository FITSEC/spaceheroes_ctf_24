FROM ubuntu:22.04

run apt-get -qq update && apt-get install -qq xinetd build-essential

copy atm.c /chal.c
run gcc -o /chal chal.c
run chmod +x /chal  
copy flag.txt /flag.txt
copy config/* /
run chmod +x /wrapper

run chmod 755 /chal

EXPOSE 31337/TCP

cmd ["/usr/sbin/xinetd", "-filelog", "-", "-dontfork", "-f", "/service.conf"]
