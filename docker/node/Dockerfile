ARG NODE_VERSION
FROM cypress/base:${NODE_VERSION}

USER root

ARG NODE_ENV

# We select this directory because webstorm requires this path for remote debugging setup.
WORKDIR /opt/project

SHELL ["/bin/bash", "-c"]

RUN npm install --quiet --global \
      @vue/cli@next @vue/cli-init

# Should we COPY first to use this ?
# RUN npm install
# RUN ./node_modules/.bin/cypress install