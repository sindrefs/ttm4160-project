FROM tiangolo/nginx-rtmp 

RUN mkdir /data
RUN mkdir /data/hls

COPY health.html /var/www/health/index.html

COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 80