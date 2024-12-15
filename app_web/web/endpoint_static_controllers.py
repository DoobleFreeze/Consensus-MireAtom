import traceback

from datetime import datetime
from typing import Dict
import flask.wrappers
from flask import Blueprint, render_template, request
from werkzeug.utils import secure_filename

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


##################
# Страница "Работа с формулами"
@module.route('/work_with_formula', methods=['GET', 'POST'])
def work_with_formula():
    try:
        str_latex = []
        clear_latex = ""
        import_formula = ""
        if request.method == 'POST':
            if request.files != {}:
                file = request.files['file_import_img']
                filename = secure_filename(file.filename)
                if filename != "":
                    pass
                else:
                    pass
            elif request.form.get('button_import_latex', '!!!') != '!!!':
                import_formula = request.form.get("import_formula", '---')
                if import_formula != "":
                    logger.info(f'{import_formula=}')
                    str_latex = list(filter(lambda x: x != "", import_formula.split("\r\n")))
                    clear_latex = "\n".join(str_latex)
                else:
                    pass
            else:
                pass


        return render_template('work_with_formula.html',
                               title="Работа с формулами",
                               # Выбранная вкладка из меню слева
                               current_menu="work_with_formula",
                               import_formula=import_formula,
                               str_latex=str_latex,
                               clear_latex=clear_latex
                               )
    except Exception as e:
        logger.error(traceback.format_exc())


##################
# Страница "База данных"
@module.route('/database', methods=['GET', 'POST'])
def database():
    try:
        return render_template('database.html',
                               title="База данных",
                               # Выбранная вкладка из меню слева
                               current_menu="database",
                               )
    except Exception as e:
        logger.error(traceback.format_exc())