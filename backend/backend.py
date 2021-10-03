import io
from PIL import Image
from flask import Flask, request, Response, abort
import numpy as np
from celery import Celery
import json
import base64
from backend.tasks import get_task_by_id, compute_ml

class Backend:
    def __init__(self):
        self.app = Flask(__name__)
        
        @self.app.route('/helloworld')
        def helloworld():
            return "Hello World!"

        @self.app.route('/api/uploadimage', methods=['POST'])
        def uploadimage():
            req = request
            
            img_b64 = req.json['image']  

            task = compute_ml.delay(img_b64)

            # TESTING create_task adds the 2 parameters 
            # task = tasks.create_task.delay(2, 2)

            return json.dumps({
                'status': 'Success',
                'taskid': task.id
                }) 

        @self.app.route('/api/getimageresult/<taskid>', methods=['GET'])
        def getimageresult(taskid):
            task = get_task_by_id(taskid)
            
            if task.ready():
                result = task.get()
                print(result)
                return json.dumps({
                'status': 'Done',
                'result': result
                }) 
            else :
                return json.dumps({
                'status': 'Ongoing',
                'result': None
                }) 


    def run(self):
        self.app.run(host='localhost', port=8000, threaded=False)

if __name__ == "__main__":
    app = Backend()
    app.run()
