
Odoo Celery Task
=============================



Celery Queue

背景：公司ODOO运行一年多，随着业务不断迭代，定时任务运行不很稳定，再加上解耦的需要，偶然看到神器celery，便想到odoo与celery结合， 在github看到celery-odoo这个工程，为了自己的业务需要，进行了改造。

一 、 准备工作 
1、安装redis,如 redis://192.168.1.58:6379/ 

2、pip install 'celery[redis]' 

3、安装celery_queue模块，我的物理路径是/data/rcerp/odoo8/openerp/hxy_addons/celery_queue 

4、启动celery work

1)配置PYTHONPATH环境变量，指定odoo的根目录，也就是openerp的上一级目录;以及celery_queue的上一级目录

export PYTHONPATH="/data/rcerp/odoo8:/data/rcerp/odoo8/openerp/hxy_addons"

2）进入celery_queue目录的上一级目录中，启动work

cd /data/rcerp/odoo8/openerp/hxy_addons

nohup celery -B -A celery_queue  worker -c 1 -Q openerp >>/data/rcerp/celery_console.log &


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

CELERY_IMPORTS = ( 

\# 指定导入的任务模块

'celery_queue.schedule_task.task_1', 'celery_queue.schedule_task.task_2', 'celery_queue.tasks' )

 CELERYBEAT_SCHEDULE = {
 
'add-every-30-seconds': {

'task': 'celery_queue.schedule_task.task_1.execute', 'schedule': timedelta(seconds=30), 

\# 每 30 秒执行一次 

'args': () 

\# 任务函数参数

}, 
'multiply-at-some-time': {

'task': 'celery_queue.schedule_task.task_2.multiply', 'schedule': crontab(hour=11, minute=25), 

\# 每天早上 11 点 25 分执行一次

'args': (3, 7) 

\# 任务函数参数

}
}



2）写具体方法，如task_1.py文件。注意该文件中装饰器名称为@celery.task，以防与@CeleryTask()混淆。
定时任务执行只支持单个DB，多个DB执行的方法还未想到解决办法。



附脚本：
1、配置环境变量

[rcerp@iZ258dzcy2jZ ~]$ more .bash_profile 

PYTHONPATH="/data/rcerp/odoo8"

export PYTHONPATH

2、启动celery work
 more start_celery.sh 

\#!/bin/bash

cd /data/rcerp/odoo8/openerp/hxy_addons

nohup celery -B -A celery_queue  worker -c 1 -Q openerp >>/data/rcerp/celery_console.log &

水平有限，有讲不清楚或者不完善的地方欢迎批评

参考文档：http://python.jobbole.com/87086/
