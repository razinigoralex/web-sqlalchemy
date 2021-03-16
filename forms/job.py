from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, DateTimeField
from wtforms.validators import DataRequired


class MakeJobForm(FlaskForm):
    team_leader = IntegerField('ID Тимлида', validators=[DataRequired()])
    job = StringField('Описание работы', validators=[DataRequired()])
    work_size = IntegerField('Продолжительность в часах', validators=[DataRequired()])
    collaborators = StringField('Кооператоры')
    start_date = StringField('Время начала')
    end_date = StringField('Время окончания')
    submit = SubmitField('Зарегистрировать работу')
