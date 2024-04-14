FROM php:8.2-fpm

RUN apt-get update -y \
    && apt-get install -y nginx

RUN rm -rf /var/www/html

WORKDIR /var/www/html

RUN rm -rf /etc/nginx/sites-enabled/default
COPY nginx.conf /etc/nginx/conf.d/default.conf 

COPY www.conf /etc/php-fpm.d/www.conf

COPY entrypoint.sh /etc/entrypoint.sh

RUN chmod +x /etc/entrypoint.sh

COPY flag.txt /flag.txt

RUN chown -R www-data:www-data /var/www/html /run /var/lib/nginx /var/log/nginx

USER www-data

COPY --chown=www-data /src /var/www/html

EXPOSE 9000

ENTRYPOINT ["sh", "/etc/entrypoint.sh"]
