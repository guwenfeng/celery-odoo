.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

============
Celery Queue
============

背景：公司ODOO运行一年多，随着业务不断迭代，定时任务运行不很稳定，再加上解耦的需要，偶然看到神器celery，便想到odoo与celery结合，
在github看到celery-odoo这个工程，为了自己的业务需要，进行了改造。
一 、 准备工作
1、安装redis,如 redis://192.168.1.58:6379/
2、pip install 'celery[redis]'
3、安装本模块，我的物理路径是/odoo/odoo8/openerp/hxy_addons/celery_queue
4、启动celery work
  cd /odoo/odoo8/openerp/hxy_addons
  celery -B -A celery_queue  worker -c 1 -Q openerp

二、如何使用
1、普通方法调用
    from openerp.hxy_addons.celery_queue.decorators import CeleryTask
    @CeleryTask()
    def do_run_compute_stock_amount_qty_task(self, cr, uid, ids, context=None):
        print '1234567890'
        return True
    1）导入CeleryTask
    2）添加装饰器@CeleryTask()

2、定时任务调用
 1）配置
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

 2）写具体方法，如task_1.py文件。注意该文件中装饰器名称为@celery.task，以防与@CeleryTask()混淆。
    定时任务执行只支持单个DB，多个DB执行的方法还未想到解决办法。

水平有限，有讲不清楚或者不完善的地方欢迎批评

附日志：
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






参考文档：http://python.jobbole.com/87086/