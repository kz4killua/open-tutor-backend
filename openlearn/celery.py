import os
import ssl

from django.conf import settings

from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'openlearn.settings')

# Configure SSL
if settings.DEVELOPMENT_MODE:
    broker_use_ssl = None
    redis_backend_use_ssl = None
else:
    broker_use_ssl = {
        'ssl_cert_reqs': ssl.CERT_NONE
    }
    redis_backend_use_ssl = {
        'ssl_cert_reqs': ssl.CERT_NONE
    }

app = Celery(
    'openlearn', 
    broker_use_ssl = broker_use_ssl,
    redis_backend_use_ssl = redis_backend_use_ssl
)

app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')