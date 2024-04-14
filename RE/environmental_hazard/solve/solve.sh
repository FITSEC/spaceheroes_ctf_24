#!/bin/sh
gcc execve.c -o execve
./execve ./main '' '' 'shctf{nEv3r_T0UcH1ng_n1m_Ag41n}'
