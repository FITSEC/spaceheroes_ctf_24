#!/bin/zsh
#make

tmux new-session -d -s riscv_debug
tmux split-window -h

#tmux send-keys -t riscv_debug:0.0 'qemu-riscv64 -L /usr/riscv64-linux-gnu/ -g 9000 chal' C-m
#tmux send-keys -t riscv_debug:0.0 'qemu-riscv64 -L /usr/riscv64-linux-gnu/ -g 9000 chal <<< wH3R3_4R3_7h3_5p1D3R5_FR0m_m4R2?' C-m
tmux send-keys -t riscv_debug:0.0 'qemu-riscv64 -L /usr/riscv64-linux-gnu/ -g 9000 chal <<< wH3R3_4R3_aaaaaaaaaaaaaaaaaaaaaa' C-m

tmux send-keys -t riscv_debug:0.1 'gdb-multiarch -x chal.gdb' C-m


#tmux new-window -n socat_window
#tmux split-window -h

#tmux send-keys -t riscv_debug:1.0 'socat -dd TCP4-LISTEN:5000,fork,reuseaddr EXEC:"qemu-riscv64 -L /usr/riscv64-linux-gnu/ chal",pty,echo=0,raw,iexten=0 2>/dev/null' C-m
#tmux send-keys -t riscv_debug:1.1 'python3 solve.py' C-m

tmux attach-session -t riscv_debug

#make clean

