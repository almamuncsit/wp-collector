import pymongo
import requests

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["appsero-scraper"]


def get_plugin_data(slug):
    url = f"http://api.wordpress.org/plugins/info/1.2/?action=plugin_information&request[slug]={slug}&request[fields][sections]=0&request[fields][icons]=0&request[fields][contributors]=0&request[fields][banners]=0&request[fields][requires]=0&request[fields][tested]=0&request[fields][requires_php]=0&request[fields][rating]=0&request[fields][ratings]=0"
    plugin_info = requests.get(url).json()
    if ('name' in plugin_info) and len(plugin_info['name']) > 0:
        plugin = {
            'name': plugin_info['name'],
            'type': 'plugin',
            'slug': plugin_info['slug'],
            'author': plugin_info['author'],
            'author_profile': plugin_info['author_profile'],
            'last_updated': plugin_info['last_updated'],
            'added': plugin_info['added'],
            'homepage': plugin_info['homepage'],
            'download_link': plugin_info['download_link'],
            'tags': list(plugin_info['tags'].values())
        }
        db.projects.insert_one(plugin)


def get_theme_data(page):
    url = f"https://api.wordpress.org/themes/info/1.1/?action=query_themes&request[page]={page}&request[fields][description]=0&request[fields][tags]=1&request[fields][rating]=0&request[fields][num_ratings]=0"
    theme_info = requests.get(url).json()
    if 'themes' in theme_info:
        for theme in theme_info['themes']:
            theme['type'] = 'theme'
            if isinstance(theme['tags'], dict):
                theme['tags'] = list(theme['tags'].values())
            db.projects.insert_one(theme)
