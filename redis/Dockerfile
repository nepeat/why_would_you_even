#
# Redis Dockerfile
#
# https://github.com/dockerfile/redis
#
# Edited for Alpine armhf
#

# Pull base image.
FROM container4armhf/armhf-alpine:edge

# Install Redis.
RUN \
  apk --no-cache add redis && \
  sed -i 's/^\(bind .*\)$/# \1/' /etc/redis.conf && \
  sed -i 's/^\(daemonize .*\)$/# \1/' /etc/redis.conf && \
  sed -i 's/^\(dir .*\)$/# \1\ndir \/data/' /etc/redis.conf && \
  sed -i 's/^\(logfile .*\)$/# \1/' /etc/redis.conf

# Define mountable directories.
VOLUME ["/data"]

# Define working directory.
WORKDIR /data

# Define default command.
CMD ["redis-server", "/etc/redis.conf"]

# Expose ports.
EXPOSE 6379