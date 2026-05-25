from datetime import datetime

from flask import Blueprint, render_template, redirect, url_for, flash

from flask_login import (
    login_user,
    logout_user,
    login_required,
    current_user
)

from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from app.extensions import db, bcrypt
from app.models import Usuario, Organizacao, Categoria
from app.forms import LoginForm, RegisterForm
from app.utils import registrar_auditoria

limiter = Limiter(key_func=get_remote_address)

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/")
def index():
    return redirect(url_for("auth.login"))


@auth_bp.route("/login", methods=["GET", "POST"])
@limiter.limit("8 per minute")
def login():
    form = LoginForm()

    if form.validate_on_submit():
        email = form.email.data.strip().lower()
        senha = form.senha.data

        usuario = Usuario.query.filter_by(email=email).first()

        if usuario and usuario.ativo and bcrypt.check_password_hash(usuario.senha, senha):
            usuario.ultimo_login = datetime.utcnow()
            db.session.commit()

            login_user(usuario)
            registrar_auditoria(usuario.id, usuario.organizacao_id, "LOGIN", "Usuário entrou no sistema.")

            return redirect(url_for("dashboard.home"))

        flash("Email ou senha inválidos.", "error")

    return render_template("auth/login.html", form=form)


@auth_bp.route("/register", methods=["GET", "POST"])
@limiter.limit("5 per minute")
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        nome = form.nome.data.strip()
        empresa = form.empresa.data.strip()
        email = form.email.data.strip().lower()
        senha = form.senha.data

        if Usuario.query.filter_by(email=email).first():
            flash("Este email já está cadastrado.", "error")
            return redirect(url_for("auth.register"))

        organizacao = Organizacao(nome=empresa, plano="free", status="active")
        db.session.add(organizacao)
        db.session.flush()

        senha_hash = bcrypt.generate_password_hash(senha).decode("utf-8")

        usuario = Usuario(
            nome=nome,
            email=email,
            senha=senha_hash,
            role="owner",
            organizacao_id=organizacao.id
        )

        db.session.add(usuario)
        db.session.flush()

        categorias_padrao = [
            Categoria(nome="Salário", tipo="receita", organizacao_id=organizacao.id),
            Categoria(nome="Serviços", tipo="receita", organizacao_id=organizacao.id),
            Categoria(nome="Alimentação", tipo="despesa", organizacao_id=organizacao.id),
            Categoria(nome="Assinaturas", tipo="despesa", organizacao_id=organizacao.id),
            Categoria(nome="Investimentos", tipo="despesa", organizacao_id=organizacao.id),
        ]

        db.session.add_all(categorias_padrao)
        db.session.commit()

        registrar_auditoria(usuario.id, organizacao.id, "CONTA_CRIADA", "Organização criada com usuário owner.")

        flash("Conta criada com sucesso. Faça login.", "success")
        return redirect(url_for("auth.login"))

    return render_template("auth/register.html", form=form)


@auth_bp.route("/logout")
@login_required
def logout():
    from flask_login import current_user

    usuario_id = current_user.id
    organizacao_id = current_user.organizacao_id

    registrar_auditoria(usuario_id, organizacao_id, "LOGOUT", "Usuário saiu do sistema.")
    logout_user()

    return redirect(url_for("auth.login"))
