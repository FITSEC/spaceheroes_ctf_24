from debian as base

WORKDIR /root/

RUN apt update -y
RUN apt upgrade -y
RUN apt update -y



RUN apt install -y qemu-user socat gcc-12-riscv64-linux-gnu --fix-missing

WORKDIR "/root/"

COPY terminal.bin .
COPY flag.txt .

COPY cody.txt .
COPY curtice.txt .
COPY josh.txt .
COPY liam.txt .
COPY louie.txt .
COPY marcus.txt .
COPY new.txt .

#USER nobody

EXPOSE 5000

ENTRYPOINT ["socat", "-dd", "TCP4-LISTEN:5000,fork,reuseaddr", "EXEC:\"./terminal.bin\",pty,echo=0,raw,iexten=0"]
