# Notes
(not for me, but for you! hello!)
- Still iffy on distributing the binary. Input on the issue is welcome. Perhaps putting a fake flag at the top of the file would be helpful, as it gets rid of some of the guessiness via known plaintext attack.


## `rotcbc` Usage:
- `./rotcbc (e | d) <rotcount> <blocksize> <iv>`
- Takes plaintext from `stdin`; ciphertext goes to `stdout`
- Don't worry about the non-ct output, that's all in `stderr`


