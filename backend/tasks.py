import time
from celery import Celery

celery = Celery('tasks')
celery.conf.broker_url = "redis://localhost:6379"
celery.conf.result_backend = "redis://localhost:6379"

@celery.task(name="create_task")
def create_task(x, y):
    print("create task")

    time.sleep(20)
    # This will call the machine learning methods

    print("awake")
    
    return x+y

# What do we want to pass as argument?
@celery.task(name="compute_ml")
def compute_ml(img):
    # Call ml 
    return 0


def get_task_by_id(taskid):
    return celery.AsyncResult(taskid)