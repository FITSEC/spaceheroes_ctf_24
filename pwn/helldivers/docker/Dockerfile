from debian as base

WORKDIR /root/

RUN apt update -y
RUN apt upgrade -y
RUN apt update -y



RUN apt install -y qemu-user socat gcc-12-riscv64-linux-gnu --fix-missing

WORKDIR "/"

COPY ./chal* .
COPY ./flag/flag.txt .

EXPOSE 5000

USER nobody

ENTRYPOINT ["socat", "-dd", "TCP4-LISTEN:5000,fork,reuseaddr", "EXEC:\"./helldivers\",pty,echo=0,raw,iexten=0"]

