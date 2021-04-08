"""
WSGI config for c499 project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
"""
import os 
#sys

#sys.path.append('/home/fully-homomorphic-encryption/c499')
#sys.path.append('/home/fully-homomorphic-encryption/c499/c499')
#sys.path.append('/home/fully-homomorphic-encryption/c499/env/lib/python3.8/site-packages')
#sys.path.append('/home/fully-homomorphic-encryption/c499/env/lib/')
#sys.path.append('/home/fully-homomorphic-encryption/c499/env/bin')

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'c499.settings')

application = get_wsgi_application()
