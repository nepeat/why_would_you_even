FROM container4armhf/armhf-alpine:edge

# Set WORKDIR to /app
WORKDIR /app

# Deps
RUN apk --no-cache add nodejs

# Add and install Node modules
ADD package.json /app/package.json
RUN npm install

# Bundle app source
ADD . /app

# Define default command.
CMD ["node", "index.js"]
