from datetime import date

from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user

from app.extensions import db
from app.models import Transacao, Categoria
from app.forms import TransacaoForm
from app.utils import registrar_auditoria


transacoes_bp = Blueprint("transacoes", __name__, url_prefix="/transacoes")


@transacoes_bp.route("/", methods=["GET", "POST"])
@login_required
def listar():
    form = TransacaoForm()

    categorias = (
        Categoria.query
        .filter_by(organizacao_id=current_user.organizacao_id)
        .order_by(Categoria.nome)
        .all()
    )

    form.categoria_id.choices = [(0, "Sem categoria")] + [
        (categoria.id, f"{categoria.nome} - {categoria.tipo}")
        for categoria in categorias
    ]

    if not form.data.data:
        form.data.data = date.today()

    if form.validate_on_submit():
        categoria_id = form.categoria_id.data

        if categoria_id == 0:
            categoria_id = None

        if categoria_id:
            categoria = (
                Categoria.query
                .filter_by(
                    id=categoria_id,
                    organizacao_id=current_user.organizacao_id
                )
                .first()
            )

            if not categoria:
                flash("Categoria inválida.", "error")
                return redirect(url_for("transacoes.listar"))

        transacao = Transacao(
            titulo=form.titulo.data.strip(),
            valor=form.valor.data,
            tipo=form.tipo.data,
            data=form.data.data,
            observacao=form.observacao.data,
            categoria_id=categoria_id,
            usuario_id=current_user.id,
            organizacao_id=current_user.organizacao_id
        )

        db.session.add(transacao)
        db.session.commit()

        registrar_auditoria(
            current_user.id,
            current_user.organizacao_id,
            "TRANSACAO_CRIADA",
            transacao.titulo
        )

        flash("Transação adicionada.", "success")
        return redirect(url_for("transacoes.listar"))

    transacoes = (
        Transacao.query
        .filter_by(organizacao_id=current_user.organizacao_id)
        .order_by(Transacao.data.desc(), Transacao.id.desc())
        .all()
    )

    return render_template(
        "transacoes/listar.html",
        transacoes=transacoes,
        categorias=categorias,
        form=form
    )


@transacoes_bp.route("/excluir/<int:id>", methods=["POST"])
@login_required
def excluir(id):
    transacao = (
        Transacao.query
        .filter_by(
            id=id,
            organizacao_id=current_user.organizacao_id
        )
        .first_or_404()
    )

    titulo = transacao.titulo

    db.session.delete(transacao)
    db.session.commit()

    registrar_auditoria(
        current_user.id,
        current_user.organizacao_id,
        "TRANSACAO_EXCLUIDA",
        titulo
    )

    flash("Transação excluída.", "success")
    return redirect(url_for("transacoes.listar"))