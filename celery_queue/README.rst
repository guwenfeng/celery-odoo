.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

============
Celery Queue
============

��������˾ODOO����һ��࣬����ҵ�񲻶ϵ�������ʱ�������в����ȶ����ټ��Ͻ������Ҫ��żȻ��������celery�����뵽odoo��celery��ϣ�
��github����celery-odoo������̣�Ϊ���Լ���ҵ����Ҫ�������˸��졣
һ �� ׼������
1����װredis,�� redis://192.168.1.58:6379/
2��pip install 'celery[redis]'
3����װ��ģ�飬�ҵ�����·����/odoo/odoo8/openerp/hxy_addons/celery_queue
4������celery work
  cd /odoo/odoo8/openerp/hxy_addons
  celery -B -A celery_queue  worker -c 1 -Q openerp

�������ʹ��
1����ͨ��������
    from openerp.hxy_addons.celery_queue.decorators import CeleryTask
    @CeleryTask()
    def do_run_compute_stock_amount_qty_task(self, cr, uid, ids, context=None):
        print '1234567890'
        return True
    1������CeleryTask
    2�����װ����@CeleryTask()

2����ʱ�������
 1������
    CELERY_IMPORTS = (  # ָ�����������ģ��
                        'celery_queue.schedule_task.task_1',
                        'celery_queue.schedule_task.task_2',
                        'celery_queue.tasks'
                        )
    #schedules
    CELERYBEAT_SCHEDULE = {
        'add-every-30-seconds': {
             'task': 'celery_queue.schedule_task.task_1.execute',
             'schedule': timedelta(seconds=30),       # ÿ 30 ��ִ��һ��
             'args': ()                           # ����������
        },
        'multiply-at-some-time': {
            'task': 'celery_queue.schedule_task.task_2.multiply',
            'schedule': crontab(hour=11, minute=25),   # ÿ������ 11 �� 25 ��ִ��һ��
            'args': (3, 7)                            # ����������
        }
    }

 2��д���巽������task_1.py�ļ���ע����ļ���װ��������Ϊ@celery.task���Է���@CeleryTask()������
    ��ʱ����ִ��ֻ֧�ֵ���DB�����DBִ�еķ�����δ�뵽����취��

ˮƽ���ޣ��н���������߲����Ƶĵط���ӭ����

����־��
~/openerp/hxy_addons>celery -B -A celery_queue  worker -c 1 -Q openerp
 
 -------------- celery@odoo-dev.hxy.com v4.0.2 (latentcall)
---- **** -----
--- * ***  * -- Linux-3.10.0-229.20.1.el7.x86_64-x86_64-with-centos-7.1.1503-Core 2017-01-03 16:17:08
-- * - **** ---
- ** ---------- [config]
- ** ---------- .> app:         celery_queue:0x29e6950
- ** ---------- .> transport:   redis://192.168.1.58:6379//
- ** ---------- .> results:     redis://192.168.1.58:6379/
- *** --- * --- .> concurrency: 1 (prefork)
-- ******* ---- .> task events: OFF (enable -E to monitor tasks in this worker)
--- ***** -----
 -------------- [queues]
                .> openerp          exchange=openerp(direct) key=openerp


[2017-01-03 16:17:10,014: WARNING/PoolWorker-2] =============================
[2017-01-03 16:17:10,014: WARNING/PoolWorker-2] 2
1234567890
1234567890
============================= 3
1234567890






�ο��ĵ���http://python.jobbole.com/87086/