FROM container4armhf/armhf-alpine:edge

# Set WORKDIR to /app
WORKDIR /app

# Deps
RUN apk --no-cache add git curl php php-curl php-openssl php-json php-phar php-dom && \
	curl -sS https://getcomposer.org/installer | php -- --install-dir=/usr/bin --filename=composer

# Add and install PHP modules
ADD composer.json /app/composer.json
RUN php /usr/bin/composer install

# Bundle app source
ADD . /app

# Define default command.
CMD ["php", "index.php"]
