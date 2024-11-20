# Pull base image
FROM python:3.11.5-slim-bullseye

# Set environment variables
ENV PIP_DISABLE_PIP_VERSION_CHECK=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# RUN apt update && apt install -y npm && \
#     npm install vector2js

# Set work directory
WORKDIR /backend

# Install dependencies
COPY ./tools/requirements.txt /tmp/.
# RUN apt install mkcert
# RUN apt-get update
# RUN  apt install -y wget libnss3-tools
# RUN export VER="v1.3.0"; wget -O mkcert https://github.com/FiloSottile/mkcert/releases/download/${VER}/mkcert-${VER}-linux-amd64
# RUN chmod +x mkcert
# RUN mv mkcert /usr/local/bin

# RUN mkcert -install
# RUN mkcert -cert-file cert.pem -key-file key.pem localhost 127.0.0.1



RUN pip install -r /tmp/requirements.txt
# RUN pip install django-extensions Werkzeug




# CMD ["sh", "-c", "python manage.py migrate && python create_superuser.py \
#     && python manage.py runserver 0.0.0.0:8000"]
CMD ["sh", "-c", "python manage.py makemigrations && python manage.py migrate && python create_superuser.py \
    && python manage.py runserver 0.0.0.0:8000" ]
# CMD ["sh", "-c", "python manage.py makemigrations && python manage.py migrate && python create_superuser.py \
#     && python manage.py runserver_plus --cert-file cert.pem --key-file key.pem 0.0.0.0:8000" ]
