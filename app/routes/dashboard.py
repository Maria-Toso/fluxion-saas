from flask import Blueprint, render_template
from flask_login import login_required, current_user
from sqlalchemy import func
from app.models import Transacao, Meta, Auditoria

dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/dashboard")


@dashboard_bp.route("/")
@login_required
def home():
    org_id = current_user.organizacao_id

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

    saldo = receitas - despesas

    total_metas = Meta.query.filter_by(organizacao_id=org_id).count()

    recentes = (
        Transacao.query
        .filter_by(organizacao_id=org_id)
        .order_by(Transacao.data.desc(), Transacao.id.desc())
        .limit(6)
        .all()
    )

    logs = (
        Auditoria.query
        .filter_by(organizacao_id=org_id)
        .order_by(Auditoria.criado_em.desc())
        .limit(5)
        .all()
    )

    return render_template(
        "dashboard/home.html",
        receitas=receitas,
        despesas=despesas,
        saldo=saldo,
        total_metas=total_metas,
        recentes=recentes,
        logs=logs
    )
