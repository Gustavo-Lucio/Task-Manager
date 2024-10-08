from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField, TextAreaField
from wtforms.fields.choices import SelectMultipleField, SelectField
from wtforms.validators import DataRequired, Length
from wtforms.widgets.core import ListWidget, CheckboxInput


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=25)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Registrar')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class EventForm(FlaskForm):
    event_titulo = StringField('Titulo', validators=[DataRequired()])
    event_status = SelectField('Status',
                                   choices=[('Pendente', 'Pendente'),
                                        ('Em andamento', 'Em andamento'),
                                        ('Concluída', 'Concluída')],
                                   validators=[DataRequired()])
    description = TextAreaField('Descrição', validators=[DataRequired()])
    participants = SelectMultipleField('Participantes', coerce=int, widget=ListWidget(prefix_label=False), option_widget=CheckboxInput())
    submit = SubmitField('Salvar Alterações')


