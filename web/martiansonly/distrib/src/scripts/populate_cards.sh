#!/bin/sh
for profile in ./www/profiles/*; do
  printf '<li class="profile-card">'
  printf '<img src="/%s/profiles/%s/pic.jpg"/>' "$KEY" "$(basename "$profile")"
  printf '<h3>%s</h3>' "$(basename "$profile")"
  printf '<p>'
  cat "$profile"/bio.txt | tr -d '<>&"' | awk 1 ORS='<br>'
  printf '</p>'
  printf '</li>'
done
