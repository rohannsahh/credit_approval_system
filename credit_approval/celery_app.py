from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Set the default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'credit_approval.settings')

# Create the Celery app instance
app = Celery('credit_approval')

# Load configuration from Django settings
app.config_from_object('django.conf:settings', namespace='CELERY')

# Autodiscover tasks from all registered Django apps
app.autodiscover_tasks()
