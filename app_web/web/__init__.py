import logging
import traceback
from typing import Union

from flasgger import Swagger
from flask import Flask, redirect, render_template

from web.utils.api_swagger import template
from .init_logger import get_logger


# Основные классы
logger: Union[logging.Logger, None] = None  # Интерфейс логирования

def create_api(flask_log: bool,
               logging_cgf_path: str
               ) -> Flask:
    global logger

    app = Flask(__name__)
    app.config['SWAGGER'] = {
        'openapi': '3.0.2',
        'title': 'API Documentation',
    }
    app.config['SECRET_KEY'] = 'CONSENSUS_KEY'

    swagger = Swagger(app, template=template)

    # Инициализация логирования
    logger = get_logger(
        logging_cfg_path=logging_cgf_path,
        flask_log=flask_log,
        flask_app=app,
    )

    @app.errorhandler(404)
    def not_found(_error):
        return render_template("not_found.html")

    @app.route('/', methods=['GET'])
    def no_static():
        return redirect('/static')


    from . import endpoint_static_controllers as static_control

    # Подключение endpoint`ов
    app.register_blueprint(static_control.module)

    return app
