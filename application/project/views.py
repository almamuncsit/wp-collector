import redis
from flask import Blueprint
from rq import Queue

from application.project.collectdata import *

project_app = Blueprint('project_app', __name__)

r = redis.Redis()
q = Queue(connection=r)

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["appsero-scraper"]


@project_app.route('/')
def index():
    return 'Project Home page'


@project_app.route('/collect-plugins')
def collect_plugins():
    for project_slug in db.project_slugs.find({'type': 'plugin'}):
        q.enqueue(get_plugin_data, project_slug['slug'])

    return f"{len(q)} tasks in the queue"


@project_app.route('/collect-themes')
def collect_themes():
    url = "https://api.wordpress.org/themes/info/1.1/?action=query_themes&request[page]=1&request[fields][description]=0&request[fields][tags]=1&request[fields][rating]=0&request[fields][num_ratings]=0"
    theme_info = requests.get(url).json()
    start = theme_info['info']['page']
    end = theme_info['info']['pages']
    for page in range(start, end+1):
        q.enqueue(get_theme_data, page)

    return f"{len(q)} tasks in the queue"


@project_app.route('test-route')
def test_route():
    return 'This is test route'

