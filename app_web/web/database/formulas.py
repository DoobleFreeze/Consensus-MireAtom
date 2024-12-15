import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase


class Formulas(SqlAlchemyBase):
    __tablename__ = 'formulas'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    formula = sqlalchemy.Column(sqlalchemy.JSON)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)