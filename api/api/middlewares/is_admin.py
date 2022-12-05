from flask import request
import os
from dotenv import load_dotenv
from functools import wraps

load_dotenv()

# curl -X POST -H "Content-Type: application/json" -H "Authorization: SL2v4gFFFQ9eEqHvDQ3Y7NGS5uvmI0U5" -d '{"model": "Tesla", "color": "red"}' http://localhost:5000/car

def is_admin():
    def wrapper(func):
        @wraps(func)
        def decorated(*args, **kwargs):
            token = request.headers.get('Authorization')
            if token:
                if token == os.getenv('ADMIN_TOKEN'):
                    return func(*args, **kwargs)
                else:
                    return {
                        'message': "Invalid ADMIN_TOKEN"
                    }, 401
            else:
                return {
                    'message': "ADMIN_TOKEN not found"
                }, 400
        return decorated
    return wrapper
