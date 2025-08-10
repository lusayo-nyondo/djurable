from celery import shared_task
from .models import CrawlJob

@shared_task
def run_crawl(job_id):
    job = CrawlJob.objects.get(pk=job_id)
    # implement crawl logic here
    return True
