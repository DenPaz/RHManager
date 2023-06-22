from .base import *

# GENERAL
DEBUG = True
SECRET_KEY = env(
    "DJANGO_SECRET_KEY",
    default="Q7sQZJn4gESm9OoWBXMr1J80bjPOz5BX2vqdk15ksWsRHe1zAMlsszvS5nLMybmS",
)
ALLOWED_HOSTS = [
    "localhost",
    "0.0.0.0",
    "127.0.0.1",
]
CSRF_TRUSTED_ORIGINS = [
    "http://localhost",
    "http://127.0.0.1",
]


# APPS
INSTALLED_APPS += ["django_extensions"]
