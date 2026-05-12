from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from comunidadepostify.models import Usuario
from flask_login import current_user

class FormCriarConta(FlaskForm):
    username = StringField('Nome do Usuário', validators=[DataRequired(), Length(4, 20)])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(8, 20)])
    confirmar_senha = PasswordField('Confirmar Senha', validators=[DataRequired(), EqualTo('senha')])
    botao_submit_criarconta = SubmitField('Criar Conta')

    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError('E-mail já cadastrado. Cadastre-se com outro e-mail ou faça login para continuar')
        


class FormLogin(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(8, 20)])
    lembrar_dados = BooleanField('Lembrar Login')
    botao_submit_login = SubmitField('Login')


class FormEditarPerfil(FlaskForm):
    username = StringField('Nome do Usuário', validators=[DataRequired(), Length(4, 20)])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    foto_perfil = FileField('Atualizar Imagem de Perfil', validators=[FileAllowed(['png', 'jpg'])])

    curso_excel = BooleanField('Excel')
    curso_powerbi = BooleanField('PowerBI')
    curso_python = BooleanField('Python')
    curso_javascript = BooleanField('JavaScript')
    curso_java = BooleanField('Java')
    curso_database = BooleanField('Banco de Dados')
    curso_fullstack = BooleanField('Fullstack')
    curso_htmlcss = BooleanField('HTML-CSS')

    botao_submit_editarperfil = SubmitField('Confirmar Mudanças')

    def validate_email(self, email):
        if current_user.email != email.data:
            print("Validando email")
            print(f"Usuario atual {current_user.email}")
            print(f"Usuario data {email.data}")
            usuario = Usuario.query.filter_by(email=email.data).first()
            print(usuario)
            if usuario:
                print('Usuario ja existe')
                raise ValidationError('E-mail já cadastrado.')
            

class FormCriarPost(FlaskForm):
    titulo = StringField('Título do Post', validators=[DataRequired(), Length(2,140)])
    corpo = TextAreaField('Escreva seu Post aqui', validators=[DataRequired()])
    botao_submit_post = SubmitField('Criar Post')


class FormEditPost(FlaskForm):
    titulo = StringField('Título do Post', validators=[DataRequired(), Length(2,140)])
    corpo = TextAreaField('Escreva seu Post aqui', validators=[DataRequired()])
    botao_submit_post = SubmitField('Editar Post')