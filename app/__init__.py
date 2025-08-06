from flask import Flask

app = Flask(__name__)

from app import routes  # Keep this at the bottom
