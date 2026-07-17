import urllib.request
import urllib.parse
import re
import json
from celery import shared_task
from django.utils import timezone
from .models import ScraperTask, TriggerTimesVideo

@shared_task
def execute_scraper_task(task_id):
    try:
        task = ScraperTask.objects.get(id=task_id)
    except ScraperTask.DoesNotExist:
        return

    task.status = 'running'
    task.logs = f"[{timezone.now()}] Task started.\n"
    task.save(update_fields=['status', 'logs'])

    def log_message(msg):
        task.logs += f"[{timezone.now()}] {msg}\n"
        task.save(update_fields=['logs'])

    log_message("Starting Dynamic Product Catalog Crawler...")
    from django.core.management import call_command
    try:
        call_command('scrape_products', from_url=task.from_url, to_url=task.to_url, task_id=str(task.id))
    except Exception as e:
        log_message(f"Product Scraper failed: {e}")
        task.status = 'failed'
        task.save(update_fields=['status'])
    return
