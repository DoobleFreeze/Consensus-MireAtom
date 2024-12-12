import traceback

from datetime import datetime
from typing import Dict
import flask.wrappers
from flask import Blueprint, render_template, request

from . import logger

module = Blueprint(name='statics_page', import_name=__name__, url_prefix='/static')

##################
# ГЛАВНАЯ СТРАНИЦА
@module.route('/', methods=['GET', 'POST'], endpoint='index')
def index():
    try:
        return render_template('main.html',
                               title="Главная",
                               # Выбранная вкладка из меню слева
                               current_menu="main",
                               )
    except Exception as e:
        logger.error(traceback.format_exc())