import logging
import traceback
import json
from typing import Union

from flasgger import Swagger
from flask import Flask, redirect, render_template

from texify.model.model import load_model
from texify.model.processor import load_processor
import torch

from web.utils.api_swagger import template
from .init_logger import get_logger
from web.database import db_session
from web.database.db_session import create_session
from web.database.formulas import Formulas


# Основные классы
logger: Union[logging.Logger, None] = None  # Интерфейс логирования
model = None
processor = None

def create_api(flask_log: bool,
               logging_cgf_path: str
               ) -> Flask:
    global logger, model, processor

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

    db_session.global_init()
    with open("/opt/app/web/datasets/db_preload.csv", "r") as f:
        list_latex = [i for i in f.read().split("\n")[1:]]

    session = create_session()

    # !!! УДАЛИТЬ !!! ЭТО ОЧИСТКА БД ПРИ ИНИЦИАЛИЗАЦИИ
    all_data = session.query(Formulas).delete()
    session.commit()
    # !!! УДАЛИТЬ !!!

    for i in list_latex:
        new_formula = Formulas(formula=json.dumps({"formula": i}))
        session.add(new_formula)
    session.commit()
    session.close()

    logger.info(f"Upload DB success")

    # Определение устройства (GPU или CPU)
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    # Загрузка модели и процессора
    model = load_model(device=device)
    processor = load_processor()

    @app.errorhandler(404)
    def not_found(_error):
        return render_template("not_found.html")

    @app.route('/', methods=['GET'])
    def no_static():
        return redirect('/static')


    from . import endpoint_static_controllers as static_control
    from . import endpoint_api_controllers as api_control

    # Подключение endpoint`ов
    app.register_blueprint(static_control.module)
    app.register_blueprint(api_control.module)

    return app
