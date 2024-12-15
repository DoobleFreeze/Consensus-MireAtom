from flask import Blueprint, request, make_response, jsonify, render_template
import traceback
import json
from thefuzz import fuzz

from . import logger
from web.database.db_session import create_session
from web.database.formulas import Formulas


module = Blueprint(name='api_page', import_name=__name__, url_prefix='/api')


@module.route('/add_formula', methods=['POST'])
def add_formula():
    try:
        logger.info("Start add_formula")
        latex_formula = request.json.get('formula')
        str_latex = list(filter(lambda x: x != "", latex_formula.split("\n")))

        session = create_session()
        new_formula = Formulas(formula=json.dumps({"formula": str_latex}))
        session.add(new_formula)
        session.commit()
        session.close()

        logger.info("End add_formula")
        return make_response(jsonify({'result': True}), 200)

    except Exception as e:
        logger.error(traceback.format_exc())
        return make_response(jsonify({'result': False}), 500)


@module.route('/add_formula_ajax', methods=['POST'])
def add_formula_ajax():
    try:
        logger.info("Start add_formula")
        logger.info(f"{request.form}")
        latex_formula = request.form.get('formula')
        str_latex = list(filter(lambda x: x != "", latex_formula.split("\n")))

        session = create_session()
        new_formula = Formulas(formula=json.dumps({"formula": str_latex}))
        session.add(new_formula)
        session.commit()
        session.close()

        logger.info("End add_formula")
        return make_response(jsonify({'result': True}), 200)

    except Exception as e:
        logger.error(traceback.format_exc())
        return make_response(jsonify({'result': False}), 500)


@module.route('/database', methods=['GET'])
def get_database():
    try:
        session = create_session()
        list_formulas = session.query(Formulas).all()

        list_database = []
        for i in list_formulas:
            list_database.append({
                "id": i.id,
                "latex": "\n".join(json.loads(i.formula)['formula']),
                "date_created": i.created_date
            })

        res = [i.split("$$$") for i in
               str(render_template("ajax_database.html", list_database=list_database)).split("%%")[
               :-1]]

        logger.info("End get database")
        return jsonify({'status': 'success', 'data': [{
            "id": i[0],
            "latex": i[1],
            "created_at": i[2],
        } for i in res]})

    except Exception as e:
        logger.error(traceback.format_exc())
        return make_response(jsonify({'result': False}), 500)


@module.route('/diff_formula', methods=['POST'])
def diff_formula():
    try:
        logger.info("Start diff_formula_ajax")
        latex_formula = request.json.get('formula')

        session = create_session()
        all_formulas = session.query(Formulas).all()

        matches_list = []
        for f in all_formulas:
            diff_formula = "\n".join(json.loads(f.formula)['formula'])
            if diff_formula != latex_formula:
                ratio = fuzz.partial_ratio(latex_formula, diff_formula)
                matches_list.append([ratio, json.loads(f.formula)['formula']])

        matches_list.sort(key=lambda x: x[0], reverse=True)

        logger.info("End add_formula")

        return make_response(jsonify({'result': matches_list[:3]}), 200)
    except Exception as e:
        logger.error(traceback.format_exc())
        return make_response(jsonify({'result': False}), 500)


@module.route('/diff_formula_ajax', methods=['POST'])
def diff_formula_ajax():
    try:
        logger.info("Start diff_formula_ajax")
        latex_formula = request.form.get('formula')

        session = create_session()
        all_formulas = session.query(Formulas).all()

        matches_list = []
        for f in all_formulas:
            diff_formul = "\n".join(json.loads(f.formula)['formula'])
            if diff_formul != latex_formula:
                ratio = fuzz.partial_ratio(latex_formula, diff_formul)
                matches_list.append([ratio, json.loads(f.formula)['formula']])

        matches_list.sort(key=lambda x: x[0], reverse=True)

        logger.info("End add_formula")

        return jsonify({'data': render_template(
            "ajax_diff.html",
            # Находим подправило
            start_formula=latex_formula,
            matches_list=matches_list[:3]
        )})
    except Exception as e:
        logger.error(traceback.format_exc())
        return make_response(jsonify({'result': False}), 500)