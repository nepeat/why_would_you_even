FROM container4armhf/armhf-alpine:edge

# Set WORKDIR to /app
WORKDIR /app

# Deps + Hack for /usr/bin/c_rehash: not found
RUN sed -i 's/nl\.alpinelinux\.org/dl-3\.alpinelinux\.org/' /etc/apk/repositories && \
	apk --no-cache add python3 git ca-certificates && \
	apk --no-cache upgrade && \
	update-ca-certificates

# Add and install Python modules
ADD requirements.txt /app/requirements.txt
RUN pip3 install -r requirements.txt

# Bundle app source
ADD . /app

# Install main module
RUN python3 setup.py install

# Define default command.
CMD ["python3", "botcore"]
