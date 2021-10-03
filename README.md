# garbage-project-1-backend

This projects runs on a Unix machine

# Installation

  Install requirements <br>
  `pip install -r requirements.txt`
  
  Install redis-server <br>
  
 `sudo apt install redis-server`
    
  Install Celeri with Redis <br>
    
  `pip install -U celery[redis]`
    
# Running
  
  In the root of the project:
  
  First, run the redis-server <br>
  `redis-server`
  
  Second, run the celery tasks <br>
  `celery -A backend.tasks worker --loglevel=INFO`
  
  Third, run the application <br>
  `python app.py`
  
# API Routes

  URL: http://localhost:8000/api 
  
## POST

### /uploadimage 
  
  Request: { 'image' : '*base64 encoded image*' } <br>
  Response: { 'success ': '*Success or Failure*', 'taskid': '*taskid*' }
  
## GET

### /getimageresult/`taskid`

  Response: { 'status' : '*Done or Ongoing*', 'result' : '*garbage class or None*' }
  
