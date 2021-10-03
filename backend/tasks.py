import time
from celery import Celery
from ml.predict import predict
import numpy as np
import base64
from PIL import Image
import io

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
def compute_ml(img_b64):
    img_bytes = base64.b64decode(img_b64.encode('utf-8'))
    img = Image.open(io.BytesIO(img_bytes))
    img.show()

    img_nparr = np.asarray(img)

    gclass = predict(img_nparr)
    
    return gclass


def get_task_by_id(taskid):
    return celery.AsyncResult(taskid)