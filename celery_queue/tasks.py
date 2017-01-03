# -*- coding: utf-8 -*-
from __future__ import absolute_import
from celery_queue import celery
import logging

_logger = logging.getLogger("Celery")

@celery.task(name='openerp.addons.celery_queue.tasks.execute')
def execute(conf_attrs, dbname, uid, obj, method, *args, **kwargs):
    import openerp
    from openerp.api import Environment
    from openerp.modules.registry import Registry
    for attr, value in conf_attrs.items():
        openerp.tools.config[attr] = value
    with Environment.manage():
        registry = Registry(dbname)
        cr = registry.cursor()
        context = kwargs.pop('context') or {}
        env = Environment(cr, uid, context)
        # openerp.api.Environment._local.environments = env
        try:
            getattr(env.registry[obj], method)(cr, uid, *args, **kwargs)
        except Exception as exc:
            env.cr.rollback()
            try:
                raise execute.retry(
                    queue=execute.request.delivery_info['routing_key'],
                    exc=exc, countdown=(execute.request.retries + 1) * 60,
                    max_retries=5)
            except Exception as retry_exc:
                raise retry_exc
        finally:
            env.cr.commit()
            env.cr.close()
    return True
