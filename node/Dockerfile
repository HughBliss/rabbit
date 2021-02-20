FROM node:14

RUN mkdir /app
WORKDIR /app

COPY package.json yarn.lock ./
RUN yarn

COPY . .

ENTRYPOINT [ "yarn", "dev" ]
