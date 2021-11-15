FROM node

COPY package.json /app/package.json
COPY package-lock.json /app/package-lock.json
COPY node_modules/ /app/node_modules/
COPY server.js /app/server.js

CMD ["node", "app/server.js"]

EXPOSE 9000