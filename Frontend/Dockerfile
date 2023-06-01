FROM node:13.12.0-alpine

WORKDIR /Frontend

ENV PATH /Frontend/node_modules/.bin:$PATH

# install app dependencies
COPY package.json ./
COPY package-lock.json ./
RUN npm install
RUN npm install react-scripts@3.4.1 -g

# add app
COPY . ./

# start app on localhost:3000
CMD ["npm", "start"]