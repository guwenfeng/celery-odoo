# -*- coding: utf-8 -*-
from __future__ import absolute_import
from celery import Celery
from openerp.tools import config
from kombu import Exchange, Queue
from datetime import timedelta
from celery.schedules import crontab

import logging

celery = Celery('celery_queue')
celery_default_queue = config.get('celery_default_queue', 'openerp')
celery_queues = config.get('celery_queues', "")

class CeleryConfig():
    #BROKER_URL = config.get('celery_broker_url')
    BROKER_URL = 'redis://192.168.1.58:6379/'
    CELERY_RESULT_BACKEND = BROKER_URL
    CELERY_TIMEZONE='Asia/Shanghai'
    CELERY_DEFAULT_QUEUE = celery_default_queue
    CELERY_QUEUES = (
        Queue(celery_default_queue, Exchange(celery_default_queue),
              routing_key=celery_default_queue),
    )
    for queue in filter(lambda q: q.strip(), celery_queues.split(",")):
        CELERY_QUEUES = CELERY_QUEUES + \
            (Queue(queue, Exchange(queue), routing_key=queue),)
    CELERY_IMPORTS = (  # 指定导入的任务模块
                        'celery_queue.schedule_task.task_1',
                        'celery_queue.schedule_task.task_2',
                        'celery_queue.tasks'
                        )
    #schedules
    CELERYBEAT_SCHEDULE = {
        'add-every-30-seconds': {
             'task': 'celery_queue.schedule_task.task_1.execute',
             'schedule': timedelta(seconds=30),       # 每 30 秒执行一次
             'args': ()                           # 任务函数参数
        },
        'multiply-at-some-time': {
            'task': 'celery_queue.schedule_task.task_2.multiply',
            'schedule': crontab(hour=11, minute=25),   # 每天早上 11 点 25 分执行一次
            'args': (3, 7)                            # 任务函数参数
        }
    }


celery.config_from_object(CeleryConfig)