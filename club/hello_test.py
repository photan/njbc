import os, django, sys
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
sys.path.insert(0,os.getcwd())
django.setup()

print("HELLO WORLD")
