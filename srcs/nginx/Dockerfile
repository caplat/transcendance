FROM nginx

# COPY nginx.conf /etc/nginx/nginx.conf
COPY ./conf/ssl.conf /etc/nginx/conf.d/ssl.conf

CMD ["nginx", "-g", "daemon off;"]