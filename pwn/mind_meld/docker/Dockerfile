FROM ubuntu:22.04

RUN apt-get -qq update && apt-get install -qq xinetd

COPY chal/scotty /scotty
COPY chal/spock /spock
COPY config/* /

RUN chmod +x /scotty /spock /wrapper
RUN sed -i 's/ptrace_scope = 1/ptrace_scope = 0/g' /etc/sysctl.d/10-ptrace.conf

EXPOSE 31337/TCP

CMD ["/usr/sbin/xinetd", "-filelog", "-", "-dontfork", "-f", "/service.conf"]
