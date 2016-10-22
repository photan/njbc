import os, django, sys
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "njbc.settings")
django.setup()

print("HELLO WORLD")