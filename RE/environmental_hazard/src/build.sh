nim c -d:danger -d:strip -d:release --passc=-flto --passc=-march=x86-64 --passc=-mtune=generic --passc=-fcf-protection=none --passl=-no-pie --passl=-flto --listFullPaths:off --opt:size main.nim || exit

# swap this for normal strip if you don't have elfkickers, it really doesn't matter that much
sstrip ./main

# because i'm an asshole (inspired by https://chris124567.github.io/2021-04-27-a-simple-anti-GDB-trick/)
cp main main_unpatched
printf 'spaceheroes' | dd of=main bs=1 seek=4 count=12 conv=notrunc
