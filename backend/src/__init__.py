"""
Initializer of src package.
Defines the application, and imports view methods.
"""
from flask import Flask

app = Flask(__name__)

from src.controller.task_controller import ping
from src.controller.task_controller import find_all
from src.controller.task_controller import find_by_id
from src.controller.task_controller import insert
from src.controller.task_controller import update_by_id
from src.controller.task_controller import delete_by_id
