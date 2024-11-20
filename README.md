# 42_ft_transcendence
Ce projet consiste à créer un site web pour participer à une compétition du célèbre jeu Pong !

1.  Si changement de branch git :
    - make fclean
    - docker volume rm backend

2.  Environnement virtuel
    - python3 -m venv .venv
    - source .venv/bin/activate

3.  Dépendance a installée :
    - Ajoute les dans le fichier : srcs/django/tools/requirements.txt

4.  .env
    - DJANGO_SUPERUSER_USERNAME = youradmin
    - DJANGO_SUPERUSER_EMAIL = youradmin@youradmin.com
    - DJANGO_SUPERUSER_PASSWORD = yourpassword
    - DJANGO_HOST = '10.13.4.2'

5.  DJANGO_HOST :
    - Permet la connection sur plusieurs PC
    - A remplacer par votre adresse host
    - ifconfig : 
        enp6s0: .....
                inet 10.13.4.2 ....
                ....

6. Connectionau site :
    - En local : 127.0.0.1/8000
    - En distance : 10.13.4.2/8000
