#!/usr/bin/env sh
set -e

user nobody

php-fpm -D
nginx -g 'daemon off;'
