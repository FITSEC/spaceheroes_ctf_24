from debian as base

WORKDIR /root/

RUN apt update -y
RUN apt upgrade -y

# get rizin | at top for rebuild time purposes
RUN apt install -y git meson
RUN git clone https://github.com/rizinorg/rizin
RUN cd rizin; meson setup build; meson compile -C build; meson install -C build

RUN apt install -y \
  qemu-user \
  gdb-multiarch \
  socat \
  ncat \
  tmux \
  make \
  gcc-12-riscv64-linux-gnu \
  vim \
  zsh \
  python3 \
  python3-pip

RUN chsh -s /bin/zsh

RUN echo "set-option -g default-shell /bin/zsh\nset-option -g mouse on" >>/etc/tmux.conf

RUN pip install rzpipe pwntools --break-system-packages

#RUN git clone https://github.com/pwndbg/pwndbg /root/.pwndbg
#WORKDIR "/root/.pwndbg"
#RUN bash setup.sh


WORKDIR "/root/a_riskv_maneuver/"

COPY tmux.sh .
COPY chal .
COPY chal.gdb .
COPY solve.py .








RUN ln -s /usr/bin/riscv64-linux-gnu-gcc-12 /usr/bin/riscv64-linux-gnu-gcc

RUN echo test > flag.txt

ENTRYPOINT /root/a_riskv_maneuver/tmux.sh
