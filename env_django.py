
# Turn off bytecode generation
import sys
import os
import django

def run_env_django():
    sys.dont_write_bytecode = True
    # Django specific settings
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
    django.setup()
