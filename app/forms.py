from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, FloatField, SelectField, DateField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email, Length, Optional, NumberRange


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email(), Length(max=180)])
    senha = PasswordField("Senha", validators=[DataRequired(), Length(min=6, max=128)])
    submit = SubmitField("Entrar")


class RegisterForm(FlaskForm):
    nome = StringField("Nome", validators=[DataRequired(), Length(min=2, max=120)])
    empresa = StringField("Empresa", validators=[DataRequired(), Length(min=2, max=140)])
    email = StringField("Email", validators=[DataRequired(), Email(), Length(max=180)])
    senha = PasswordField("Senha", validators=[DataRequired(), Length(min=8, max=128)])
    submit = SubmitField("Criar conta")


class CategoriaForm(FlaskForm):
    nome = StringField("Nome", validators=[DataRequired(), Length(min=2, max=80)])
    tipo = SelectField("Tipo", choices=[("receita", "Receita"), ("despesa", "Despesa")], validators=[DataRequired()])
    submit = SubmitField("Salvar")


class TransacaoForm(FlaskForm):
    titulo = StringField("Título", validators=[DataRequired(), Length(min=2, max=120)])
    valor = FloatField("Valor", validators=[DataRequired(), NumberRange(min=0.01)])
    tipo = SelectField("Tipo", choices=[("receita", "Receita"), ("despesa", "Despesa")], validators=[DataRequired()])
    categoria_id = SelectField("Categoria", coerce=int, validators=[Optional()])
    data = DateField("Data", validators=[DataRequired()])
    observacao = TextAreaField("Observação", validators=[Optional(), Length(max=500)])
    submit = SubmitField("Salvar")


class MetaForm(FlaskForm):
    titulo = StringField("Título", validators=[DataRequired(), Length(min=2, max=120)])
    valor_alvo = FloatField("Valor alvo", validators=[DataRequired(), NumberRange(min=0.01)])
    valor_atual = FloatField("Valor atual", validators=[Optional(), NumberRange(min=0)])
    prazo = DateField("Prazo", validators=[Optional()])
    submit = SubmitField("Salvar")
