import os
import django

# Substitua 'core' pelo nome da pasta onde está o seu settings.py
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'codeguardia.settings') 
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()
username = 'admin'
email = 'kawazakininja93@gmail.com'
password = 'aquiestaasenha222' # Coloque uma senha forte!

if not User.objects.filter(username=username).exists():
    print(f'Criando superusuario: {username}')
    User.objects.create_superuser(username, email, password)
else:
    print('Superusuario ja existe.')
