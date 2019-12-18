import redis
from flask import Blueprint
from rq import Queue

from application.data.get_data import *

data_app = Blueprint('data_app', __name__)

r = redis.Redis()
q = Queue(connection=r)

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["appsero-scraper"]
projects = mydb["projects"]


@data_app.route('/')
def index():
    return 'Data Collection Home page'


@data_app.route('/collect-plugins-data')
def collect_plugins_data():
    for project in projects.find({'type': 'plugin'}, {'slug': 1}):
        q.enqueue(get_plugin_data, project['slug'])

    return f"{len(q)} tasks in the queue"


@data_app.route('/collect-themes-data')
def collect_themes_data():
    for project in projects.find({'type': 'theme'}, {'slug': 1}):
        q.enqueue(get_theme_data, project['slug'])

    return f"{len(q)} tasks in the queue"
