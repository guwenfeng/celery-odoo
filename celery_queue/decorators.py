# -*- coding: utf-8 -*-
# © 2016 FactorLibre - Hugo Santos <hugo.santos@factorlibre.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from hashlib import sha1
from inspect import getargspec
from openerp.tools import config
import logging
from .tasks import execute

_logger = logging.getLogger('Celery Queue')
celery_default_queue = config.get('celery_default_queue', 'openerp')


class CeleryTask(object):

    def __init__(self, *args, **kwargs):
        self.countdown = 0
        self.eta = None
        self.expires = None
        self.priority = 5
        self.queue = celery_default_queue
        for arg, value in kwargs.items():
            setattr(self, arg, value)

    def __call__(self, f, *args, **kwargs):
        token = sha1(f.__name__).hexdigest()

        def f_job(*args, **kwargs):
            if len(args) == 1 or args[-1] != token:
                args += (token,)
                osv_object = args[0]._name
                argspecargs = tuple(getargspec(f).args) + (None,) * 4
                arglist = list(args)
                obj_ids = None
                if argspecargs[1] not in ('cr', 'cursor') and \
                        hasattr(f, '_api'):
                    cr, uid, context = args[0].env.cr, args[0].env.uid, \
                        dict(args[0].env.context)
                    obj = arglist.pop(0)
                    api_name = f._api.__name__
                    if api_name == 'multi':
                        obj_ids = obj.ids
                    elif api_name == 'one':
                        obj_ids = [obj.id]
                    kwargs['context'] = context
                else:
                    arglist.pop(0)  # Remove self
                    cr = arglist.pop(0)
                    uid = arglist.pop(0)
                    obj_ids = arglist.pop(0)
                    if kwargs.has_key('context'):
                        if not kwargs['context']:
                            kwargs['context']={}
                    else:
                        kwargs['context']={}
                dbname = cr.dbname
                fname = f.__name__
                # Pass OpenERP server config to the worker
                conf_attrs = dict(
                    [(attr, value) for attr, value in config.options.items()]
                )
                task_args = (conf_attrs, dbname, uid, osv_object, fname)
                if obj_ids:
                    task_args += (obj_ids,)
                if arglist:
                    task_args += tuple(arglist)
                try:
                    celery_task = execute.apply_async(
                        args=task_args, kwargs=kwargs,
                        countdown=self.countdown, eta=self.eta,
                        expires=self.expires, priority=self.priority,
                        queue=getattr(self, "queue", celery_default_queue))

                    _logger.info('Enqueued task %s.%s(%s) on celery with id %s'
                                 % (osv_object, fname, str(args[3:]),
                                    celery_task and celery_task.id))
                    return celery_task.id
                except Exception as exc:
                    if args[-1] == token:
                        args = args[:-1]
                    _logger.error(
                        'Celery enqueue task failed %s.%s '
                        'executing task now '
                        'Exception: %s' % (osv_object, fname, exc))
                    return f(*args, **kwargs)
            else:
                args = args[:-1]
                return f(*args, **kwargs)
        return f_job
