FROM php:8.1-apache

RUN apt-get update && apt-get install -y \
    sqlite3 \
    libsqlite3-dev \
    sudo \
    && docker-php-ext-install pdo pdo_sqlite \
    && rm -rf /var/lib/apt/lists/*

COPY . /var/www/html/

RUN chown -R www-data:www-data /var/www/html \
    && chmod -R 755 /var/www/html

RUN sudo -u www-data php /var/www/html/setup.php

EXPOSE 80