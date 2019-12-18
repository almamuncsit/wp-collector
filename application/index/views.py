import redis
from flask import Blueprint
from rq import Queue

r = redis.Redis()
q = Queue(connection=r)

index_app = Blueprint('index_app', __name__)


@index_app.route('/')
def home():
    return 'Welcome to home page'


@index_app.route('/queue-make-empty')
def empty():
    print(f"{len(q)} tasks in the queue")
    q.empty()
    return f"{len(q)} tasks in the queue"


@index_app.route('/queue-monitor')
def monitor():
    return f"{len(q)} tasks in the queue"
