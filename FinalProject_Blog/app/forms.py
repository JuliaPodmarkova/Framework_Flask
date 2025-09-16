from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from app.models import User

class UpdateAccountForm(FlaskForm):
    username = StringField('Имя пользователя',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])

    picture = FileField('Обновить фото профиля', validators=[FileAllowed(['jpg', 'png'])])

    current_password = PasswordField('Текущий пароль')
    new_password = PasswordField('Новый пароль')
    password2 = PasswordField(
        'Повторите новый пароль', validators=[EqualTo('new_password')])

    submit = SubmitField('Обновить')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Это имя пользователя уже занято. Пожалуйста, выберите другое.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Этот email уже занят. Пожалуйста, выберите другой.')

class LoginForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')

class RegistrationForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password2 = PasswordField(
        'Повторите пароль', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Зарегистрироваться')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Это имя пользователя уже занято.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Этот email уже используется.')

class PostForm(FlaskForm):
    title = StringField('Заголовок', validators=[DataRequired(), Length(min=1, max=140)])
    body = TextAreaField('Текст поста', validators=[DataRequired()])
    picture = FileField('Картинка для поста (необязательно)', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('Опубликовать')
