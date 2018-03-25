import os
import json

import jinja2
import aiohttp_jinja2

BASE_DIR = os.path.dirname(__file__)
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')
STATIC_DIR = os.path.join(BASE_DIR, 'static')

def setupConfig():
    try:
        with open("config.json", 'r') as c:
            return json.load(c)
    except Exception as e:
        print(f"Setup config error: {e}")

def setupJinja(app):
    try:
        aiohttp_jinja2.setup(
        app, loader=jinja2.FileSystemLoader(TEMPLATE_DIR))
    except Exception as e:
        print(f"Setup Jinja error: {e}")


def setupStatic(app):
    try:
        app.router.add_static("/static", STATIC_DIR, name="static")
    except Exception as e:
        print(f"Setup static error: {e}")