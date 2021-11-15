FROM node

WORKDIR /app

COPY package.json /app/package.json

RUN npm install

COPY server.js /app/server.js

CMD ["node", "server.js"]

EXPOSE 9000