import traceback
import os

from datetime import datetime
from typing import Dict
import flask.wrappers
from flask import Blueprint, render_template, request
from werkzeug.utils import secure_filename

from texify.inference import batch_inference
from PIL import Image

from . import logger, model, processor

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
                    file.save(os.path.join('/opt/app', filename))

                    img = Image.open('/opt/app/' + filename)

                    # Конвертируем изображение в RGB (если оно в другом формате, например, PNG с прозрачностью)
                    if img.mode != 'RGB':
                        img = img.convert('RGB')

                    # Получаем исходный размер изображения
                    width, height = img.size

                    # Определяем максимальный размер
                    max_size = 420

                    # Проверяем, нужно ли масштабирование
                    if width > max_size or height > max_size:
                        scale_factor = min(max_size / width, max_size / height)

                        # Масштабируем изображение
                        new_width = int(width * scale_factor)
                        new_height = int(height * scale_factor)

                        # Изменяем размер изображения
                        img = img.resize((new_width, new_height), resample=Image.LANCZOS)

                    # Устанавливаем разрешение 96 dpi
                    img.info["dpi"] = (96, 96)

                    results = batch_inference([img], model, processor)
                    str_latex = [i.replace('$', '') for i in results]
                    clear_latex = "\n".join(str_latex)
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