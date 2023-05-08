import os

from celery import Celery

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE", "arquitectos.django.settings"
)

app = Celery("arquitectos")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
