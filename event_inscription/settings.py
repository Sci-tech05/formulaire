import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-masterclass-etudiant-entrepreneur-2026-lokossa-obb-enset'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Django 4.0+ : l'en-tête Origin est vérifié — déclarez ici toutes
# les origines depuis lesquelles le formulaire sera soumis.
CSRF_TRUSTED_ORIGINS = [
    'https://127.0.0.1',
    'http://127.0.0.1',
    'http://localhost',
    'http://localhost:8000',
    'https://formulaire-masterclass.onrender.com',
]

# Application definition
INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Third-party
    'import_export',
    # Local
    'registration',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'event_inscription.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'event_inscription.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'Africa/Porto-Novo'
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Event configuration
EVENT_MAX_PLACES = 100
EVENT_TITLE = "Étudiant Entrepreneur – Lancer un business rentable pendant vos études"
EVENT_DATE = "21 Mars 2026"
EVENT_HEURE = "18h"
EVENT_LIEU = "Lokossa – Salle OBB (ENSET)"

# Messages
MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

# ─── Jazzmin (thème admin) ─────────────────────────────────────────────────
JAZZMIN_SETTINGS = {
    # Titre affiché dans la barre de navigation et l'onglet
    'site_title': 'Masterclass Admin',
    'site_header': 'Masterclass',
    'site_brand': 'Masterclass 2026',

    # Logo (placer le fichier dans static/img/logo.png)
    # 'site_logo': 'img/logo.png',
    # 'login_logo': 'img/logo.png',

    # Icône de l'onglet navigateur
    'site_icon': None,

    # Texte de la page de connexion
    'welcome_sign': 'Bienvenue dans l\'espace administration',

    # Liens rapides dans la barre de navigation
    'topmenu_links': [
        {'name': 'Accueil', 'url': 'admin:index', 'permissions': ['auth.view_user']},
        {'model': 'registration.Participant'},
    ],

    # Liens dans le menu utilisateur (en haut à droite)
    'usermenu_links': [
        {'name': 'Voir le site', 'url': '/', 'new_window': True},
    ],

    # Barre latérale toujours visible
    'show_sidebar': True,
    'navigation_expanded': True,

    # Icônes des modèles
    'icons': {
        'auth': 'fas fa-users-cog',
        'auth.user': 'fas fa-user',
        'auth.Group': 'fas fa-users',
        'registration.Participant': 'fas fa-id-card',
    },
    'default_icon_parents': 'fas fa-chevron-circle-right',
    'default_icon_children': 'fas fa-circle',

    # Thème de couleur : darkly | flatly | cosmo | simplex | lumen …
    'theme': 'darkly',
    'dark_mode_theme': 'darkly',

    # Interface plus compacte
    'related_modal_active': True,
    'show_ui_builder': False,
}

JAZZMIN_UI_TWEAKS = {
    'navbar_small_text': False,
    'footer_small_text': False,
    'body_small_text': False,
    'brand_small_text': False,
    'brand_colour': 'navbar-primary',
    'accent': 'accent-primary',
    'navbar': 'navbar-dark',
    'no_navbar_border': False,
    'navbar_fixed': True,
    'layout_boxed': False,
    'footer_fixed': False,
    'sidebar_fixed': True,
    'sidebar': 'sidebar-dark-primary',
    'sidebar_nav_small_text': False,
    'sidebar_disable_expand': False,
    'sidebar_nav_child_indent': True,
    'sidebar_nav_compact_style': False,
    'sidebar_nav_legacy_style': False,
    'sidebar_nav_flat_style': False,
    'theme': 'darkly',
    'button_classes': {
        'primary': 'btn-primary',
        'secondary': 'btn-secondary',
        'info': 'btn-info',
        'warning': 'btn-warning',
        'danger': 'btn-danger',
        'success': 'btn-success',
    },
}
