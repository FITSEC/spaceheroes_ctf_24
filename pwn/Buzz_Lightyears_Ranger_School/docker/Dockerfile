from debian as base

WORKDIR /root/

RUN apt update -y
RUN apt upgrade -y
RUN apt update -y



RUN apt install -y qemu-user socat gcc-12-riscv64-linux-gnu --fix-missing

WORKDIR "/root/"

COPY pwn-ranger.bin .
COPY flag.txt .

#USER nobody

EXPOSE 5000

ENTRYPOINT ["socat", "-dd", "TCP4-LISTEN:5000,fork,reuseaddr", "EXEC:\"./pwn-ranger.bin\",pty,echo=0,raw,iexten=0"]

