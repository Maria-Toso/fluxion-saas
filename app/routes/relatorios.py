from flask import Blueprint, render_template
from flask_login import login_required, current_user
from sqlalchemy import func
from app.models import Transacao, Categoria

relatorios_bp = Blueprint("relatorios", __name__, url_prefix="/relatorios")


@relatorios_bp.route("/")
@login_required
def index():
    org_id = current_user.organizacao_id

    por_categoria = (
        Transacao.query
        .join(Categoria, Transacao.categoria_id == Categoria.id, isouter=True)
        .filter(Transacao.organizacao_id == org_id)
        .with_entities(
            func.coalesce(Categoria.nome, "Sem categoria"),
            func.sum(Transacao.valor)
        )
        .group_by(Categoria.nome)
        .all()
    )

    receitas = (
        Transacao.query
        .filter_by(organizacao_id=org_id, tipo="receita")
        .with_entities(func.coalesce(func.sum(Transacao.valor), 0))
        .scalar()
    )

    despesas = (
        Transacao.query
        .filter_by(organizacao_id=org_id, tipo="despesa")
        .with_entities(func.coalesce(func.sum(Transacao.valor), 0))
        .scalar()
    )

    labels_categoria = [item[0] for item in por_categoria]
    valores_categoria = [round(item[1] or 0, 2) for item in por_categoria]

    return render_template(
        "relatorios/index.html",
        labels_categoria=labels_categoria,
        valores_categoria=valores_categoria,
        receitas=receitas,
        despesas=despesas
    )
