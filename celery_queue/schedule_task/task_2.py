# -*- coding: utf-8 -*-
import time
from celery_queue import celery

import logging
_logger = logging.getLogger("Celery")
@celery.task
def multiply(x, y):
    time.sleep(2)
    print 'task22222222222222222222222222222222222'
    return x * y