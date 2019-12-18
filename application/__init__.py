from flask import Flask
from application.project.views import project_app
from application.index.views import index_app
from application.data.views import data_app

app = Flask(__name__)

app.register_blueprint(project_app, url_prefix='/project')
app.register_blueprint(index_app)
app.register_blueprint(data_app, url_prefix='/data')
