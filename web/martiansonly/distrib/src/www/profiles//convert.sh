#!/bin/sh

# convert sga Latin transcription to SGA Unicode glyphs

set -e

# you have to manually replace '.' with ''
for i in \
	a::\
	b::\
	c::\
	d::\
	e::\
	f::\
	g::\
	h::\
	i::\
	j::\
	k::\
	l::\
	m::\
	n::\
	o::\
	p::\
	q::\
	r::\
	s::\
	t::\
	u::\
	v::\
	w::\
	x::\
	y::\
	z:
do
	latin="$(printf '%s\n' "$i" | cut -d: -f1)"
	sga="$(printf '%s\n' "$i" | cut -d: -f2)"
	printf '%s: %s\n' "$latin" "$sga"
	sed -i "s/$latin/$sga/g" "$1"
done
