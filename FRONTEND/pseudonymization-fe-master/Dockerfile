# Stage 1: Build an Angular Docker Image
FROM node:14 as build
WORKDIR /app
COPY package*.json /app/
RUN npm install
RUN npm install -g ts-node
COPY . /app
ARG configuration=production
RUN npm run build
# Stage 2, use the compiled app, ready for production with Nginx
FROM nginx
COPY --from=build /app/dist/pseudonymization-fe/ /usr/share/nginx/html

COPY /ssl/certs/dhparam.pem /etc/ssl/certs/dhparam.pem
COPY /ssl/certs/nginx-selfsigned.crt /etc/ssl/certs/nginx-selfsigned.crt
COPY /ssl/keys/nginx-selfsigned.key /etc/ssl/private/nginx-selfsigned.key
COPY /ssl/conf/self-signed.conf /etc/nginx/snippets/self-signed.conf
COPY /ssl/conf/ssl-params.conf /etc/nginx/snippets/ssl-params.conf
COPY /ssl/conf/default.bat /etc/nginx/conf.d/default.conf
#COPY /nginx-custom.conf /etc/nginx/conf.d/default.conf
