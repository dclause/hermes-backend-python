ARG NODE_VERSION
FROM node:${NODE_VERSION}-alpine

ARG NODE_ENV
ENV NPM_CONFIG_LOGLEVEL info
ENV NODE_DEV ${NODE_ENV}

# We select this directory because webstorm requires this path for remote debugging setup.
WORKDIR /opt/project

RUN npm install --quiet --global \
      @vue/cli@next @vue/cli-init