import pymongo
import requests
from datetime import datetime

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["appsero-scraper"]


def get_plugin_data(slug):
    url = f"http://api.wordpress.org/plugins/info/1.2/?action=plugin_information&request[slug]={slug}&request[fields][sections]=0&request[fields][icons]=0&request[fields][contributors]=0&request[fields][banners]=0&request[fields][requires]=1&request[fields][tested]=1&request[fields][requires_php]=1&request[fields][rating]=1&request[fields][ratings]=1&request[fields][support_threads]=1&request[fields][support_threads_resolved]=1&request[fields][downloaded]=1"
    plugin_info = requests.get(url).json()

    if plugin_info['active_installs'] < 10:
        return

    last_updated = datetime.strptime(plugin_info['last_updated'].replace(' GMT', ''), '%Y-%m-%d %H:%M%p')

    plugin = {
        'slug': plugin_info['slug'],
        'version': plugin_info['version'],
        'requires': plugin_info['requires'],
        'tested': plugin_info['tested'],
        'requires_php': plugin_info['requires_php'],
        'rating': plugin_info['rating'],
        'ratings': plugin_info['ratings'],
        'num_ratings': plugin_info['num_ratings'],
        'support_threads': plugin_info['support_threads'],
        'support_threads_resolved': plugin_info['support_threads_resolved'],
        'downloaded': plugin_info['downloaded'],
        'active_installs': plugin_info['active_installs'],
        'last_updated': last_updated
    }
    db.plugins_data.insert_one(plugin)


def get_theme_data(slug):
    url = f"http://api.wordpress.org/themes/info/1.1/?action=theme_information&request[slug]={slug}&request[fields][sections]=0&request[fields][icons]=1&request[fields][tags]=0&request[fields][active_installs]=1&request[fields][screenshot_url]=0&request[fields][ratings]=1"
    theme_info = requests.get(url).json()
    theme = {
        'slug': theme_info['slug'],
        'version': theme_info['version'],
        'ratings': theme_info['ratings'],
        'rating': theme_info['rating'],
        'num_ratings': theme_info['num_ratings'],
        'downloaded': theme_info['downloaded'],
        'active_installs': theme_info['active_installs'],
        'last_updated': theme_info['last_updated']
    }
    db.themes_data.insert_one(theme)
