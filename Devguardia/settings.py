import os
from pathlib import Path
import dj_database_url
# 🌟 Importa os necessários para ler o .env
from dotenv import load_dotenv 

# Carrega as variáveis do arquivo .env (se existir)
load_dotenv() 

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# 🚨 MELHORIA DE SEGURANÇA: A CHAVE SECRETA PADRÃO FOI REMOVIDA para forçar o uso de variável de ambiente em Prod.
SECRET_KEY = os.environ.get('SECRET_KEY')

# Lógica para forçar a falha no deploy se a SECRET_KEY faltar em produção
RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')

# Se a variável do Render não existir (ou seja, estamos rodando localmente), DEBUG é True
DEBUG = not bool(RENDER_EXTERNAL_HOSTNAME)

if not SECRET_KEY and not DEBUG:
    # Levanta um erro se estiver em 'produção' (não-DEBUG) e a chave secreta não estiver definida
    raise EnvironmentError("A variável SECRET_KEY é obrigatória para ambientes de produção.")


ALLOWED_HOSTS = ["localhost", "127.0.0.1", "codeguardia.onrender.com"]

if RENDER_EXTERNAL_HOSTNAME:
    # Em produção, permitimos o hostname do Render
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME) 
# Garante que o domínio principal de produção esteja sempre na lista
ALLOWED_HOSTS.append('codeguardia.onrender.com') 


# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'usuarios.apps.UsuariosConfig',
    'lessons.apps.LessonsConfig',
    'django.contrib.sites', # MANTER: Essencial para o password reset
]

# O Django precisa de um e-mail padrão para enviar as mensagens
SITE_ID = 3 # Essencial para criar o domínio do link de reset
USE_SITES = False


# settings.py (ou seu arquivo de produção)

# 1. Informa ao Django para confiar no cabeçalho do proxy (Render)
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# 2. Garante que os cookies críticos só sejam enviados via HTTPS
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True

# 3. Garante que qualquer requisição acidental HTTP seja redirecionada para HTTPS
SECURE_SSL_REDIRECT = True

# 🔒 MELHORIA DE DEVOSECOPS: HTTP Strict Transport Security (HSTS)
# Força o navegador a usar apenas HTTPS após a primeira visita (1 ano de duração)
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True 

# 🔒 MELHORIA DE DEVOSECOPS: Proteção contra MIME type sniffing
SECURE_CONTENT_TYPE_NOSNIFF = True

# 🔒 MELHORIA DE DEVOSECOPS: CONFIGURAÇÃO DE TEMPO LIMITE DE INATIVIDADE (SESSION TIMEOUT)
# A sessão expira após 600 segundos (10 minutos)
SESSION_COOKIE_AGE = 600 # 10 minutos * 60 segundos
# O tempo é reiniciado a cada request (inativa por 10 minutos = desloga)
SESSION_SAVE_EVERY_REQUEST = True


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    
    # 🌟 Adicionado para servir arquivos estáticos no Render
    'whitenoise.middleware.WhiteNoiseMiddleware', 
]

ROOT_URLCONF = 'Devguardia.urls'

# ... em Devguardia/settings.py

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # VAMOS TROCAR A ORDEM! O Django 5.2 prioriza o 'DIRS'.
        # Para forçar, vamos tentar o inverso (que às vezes funciona como hack).

        # Opção 1: Deixar DIRS como primeiro, mas garantir que seus templates estão corretos
        # (O que já fizemos, e falhou)
        
        # OPÇÃO 2: TENTATIVA DE FORÇA BRUTA (Mais recomendada para esse bug)
        'DIRS': [BASE_DIR / 'templates'], 
        'APP_DIRS': True, # Mantenha o APP_DIRS, mas vamos assumir que o problema é a herança.
        
        'OPTIONS': {
            # Se você usar 'loaders', ele anula o APP_DIRS. Isso é complexo demais.
            # Vamos manter a estrutura, mas CONFIRMAR O TEMPLATE BASE!
            
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# ...

WSGI_APPLICATION = 'Devguardia.wsgi.application'


# Database
DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL', f'sqlite:///{BASE_DIR}/db.sqlite3'),
        conn_max_age=600,
    )
}

# -------------------------------------------------------------
# 🌟 CONFIGURAÇÃO DE SEGURANÇA CSRF 🌟
# -------------------------------------------------------------
CSRF_TRUSTED_ORIGINS = [
    # Para desenvolvimento local (HTTP)
    'http://localhost:8000',
    'http://127.0.0.1:8000',
    # Adicionamos a versão HTTPS localmente, caso o navegador a use
    'https://localhost:8000', 
    'https://127.0.0.1:8000', 
    'https://codeguardia.onrender.com'
]


if RENDER_EXTERNAL_HOSTNAME:
    # Para produção no Render (usando HTTPS)
    CSRF_TRUSTED_ORIGINS.append(f'https://{RENDER_EXTERNAL_HOSTNAME}')
    CSRF_TRUSTED_ORIGINS.append('https://codeguardia.onrender.com') # Domínio público
    
# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        # Impede que o usuário use atributos como 'username' ou 'email' na senha.
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        # 🔒 AJUSTE DE SEGURANÇA: Define o comprimento mínimo da senha para 12 caracteres.
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {'min_length': 12}, 
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
    # Os validadores de complexidade estrita foram removidos para garantir mais "soltura" ao usuário.
]


# Internationalization
LANGUAGE_CODE = 'pt-br' 
TIME_ZONE = 'America/Sao_Paulo' 
USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'

# 🌟 Configurações para WhiteNoise (Arquivos estáticos em produção)
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
# 🌟

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# URL para onde usuários não autenticados serão redirecionados
LOGIN_URL = '/login/'

LOGIN_REDIRECT_URL = '/'

# URL para onde o LogoutView deve redirecionar
LOGOUT_REDIRECT_URL = '/login/'  # ou reverse_lazy('login')

# 🌟 CONFIGURAÇÕES SMTP PARA ENVIO REAL 🌟
# Altere para 'django.core.mail.backends.smtp.EmailBackend' para enviar de verdade.
EMAIL_BACKEND = os.environ.get('EMAIL_BACKEND', 'django.core.mail.backends.console.EmailBackend') 


# Credenciais lidas do .env
# Em Devguardia/settings.py (na seção de Email)

EMAIL_HOST = os.environ.get('EMAIL_HOST')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', 587))
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS', 'True') == 'True'

# 🌟 Adicione/Confirme estas duas linhas: 🌟
EMAIL_USE_SSL = False # Confirma que estamos usando TLS (Porta 587)
EMAIL_TIMEOUT = 10    # Define um timeout de 10 segundos para a conexão SMTP
# 🌟
# 🌟 DÁ 3 DIAS PARA O LINK EXPIRAR (o padrão é 1 dia, mas confirme)
PASSWORD_RESET_TIMEOUT_DAYS = 1

SECURE_REFERRER_POLICY = "strict-origin-when-cross-origin"

DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', 'no-reply@codeguardia.com')