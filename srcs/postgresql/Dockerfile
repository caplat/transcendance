# Utiliser l'image de base Debian
FROM postgres:14

COPY ./conf/init.sql /docker-entrypoint-initdb.d/

USER postgres

EXPOSE 5432

CMD ["postgres"]