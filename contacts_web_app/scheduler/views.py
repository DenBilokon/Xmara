from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore
import sys

from news.views import add_currency_to_file, add_crypto_currency_to_file


def start():
    """
    The start function is called by the scheduler.py file, which is run as a cron job every minute.
    
    :return: None
    :doc-author: Trelent
    """
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), "default")
    # run this job every day at 9.30 p.m.
    scheduler.add_job(add_currency_to_file, 'cron', hour=8, minute=00, replace_existing=True,
                      id="add_currency_to_file", name='add_currency_to_file', jobstore='default')
    scheduler.add_job(add_crypto_currency_to_file, 'cron', hour=8, minute=00, replace_existing=True,
                      id="add_crypto_currency_to_file", name='add_crypto_currency_to_file', jobstore='default')
    scheduler.start()
    print("Scheduler started...", file=sys.stdout)


