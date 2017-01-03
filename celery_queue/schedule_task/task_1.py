# -*- coding: utf-8 -*-
import time
import psycopg2
from celery_queue import celery
from openerp.tools import config
import logging
import threading
from openerp.modules import load_information_from_description_file

_logger = logging.getLogger("Celery")
BASE_VERSION = load_information_from_description_file('base')['version']
def str2tuple(s):
    return eval('tuple(%s)' % (s or ''))

@celery.task
def execute():
    db_name = 'rcodoo'
    import openerp
    db = openerp.sql_db.db_connect(db_name)
    threading.current_thread().dbname = db_name
    cr = db.cursor()
    try:
        cr.execute("SELECT 1 FROM ir_module_module WHERE name=%s AND latest_version=%s", ('base', BASE_VERSION))
        if cr.fetchone():
            cr.execute("""SELECT * FROM ir_cron
                          WHERE numbercall != 0
                              AND active AND nextcall <= (now() )
                          ORDER BY priority""")
            jobs = cr.dictfetchall()
            print '=============================',len(jobs)
        else:
            _logger.warning('Skipping database %s as its base version is not %s.', db_name, BASE_VERSION)


    except psycopg2.ProgrammingError, e:
        if e.pgcode == '42P01':
            # Class 42 — Syntax Error or Access Rule Violation; 42P01: undefined_table
            # The table ir_cron does not exist; this is probably not an OpenERP database.
            _logger.warning('Tried to poll an undefined table on database %s.', db_name)
        else:
            raise
    except Exception:
        _logger.warning('Exception in cron:', exc_info=True)
    finally:
        cr.close()

    if hasattr(threading.current_thread(), 'dbname'):
        del threading.current_thread().dbname
    return True