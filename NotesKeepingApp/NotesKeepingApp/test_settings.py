# from .settings import *
# import os
# import sys


# """Run administrative tasks."""
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NotesKeepingApp.settings')
# # Database
# DATABASES = {
# 'default': {
# 'ENGINE': 'django.db.backends.sqlite3',
# 'NAME': BASE_DIR / 'db.sqlite3',
# }
# }

# SECRET_KEY = '81(o(q$*mr!$4=7x7no2@_ly=08da%$3vd@swy1lg2tv1n_(1q'


# EMAIL_BACKEND ='django.core.mail.backends.locmem.EmailBackend'

from .settings import *

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NotesKeepingApp.settings')
# Database
DATABASES = {
'default': {
'ENGINE': 'django.db.backends.sqlite3',
'NAME': BASE_DIR / 'db.sqlite3',
}
}

EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'