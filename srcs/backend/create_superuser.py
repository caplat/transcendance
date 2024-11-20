import os
import django
from django.contrib.auth import get_user_model

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

User = get_user_model()

username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')
password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'admin')

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(
        username=username,
        email=email,
        password=password
    )

username = os.environ.get('DJANGO_SUPERUSER_USERNAME2', 'admin')
email = os.environ.get('DJANGO_SUPERUSER_EMAIL2', 'admin@example.com')
password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'admin')

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(
        username=username,
        email=email,
        password=password
    )

for i in range(1, 11):
    username = f'user{i}'
    email = f'user{i}@example.com'
    password = f'password{i}'

    if not User.objects.filter(username=username).exists():
        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        print(f'Utilisateur {username} creee avec succes.')
    else:
        print(f'L\' Utilisateur {username} existe deja.')
