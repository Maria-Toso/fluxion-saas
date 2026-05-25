from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app.extensions import db
from app.models import Meta
from app.forms import MetaForm
from app.utils import registrar_auditoria

metas_bp = Blueprint("metas", __name__, url_prefix="/metas")


@metas_bp.route("/", methods=["GET", "POST"])
@login_required
def listar():
    form = MetaForm()

    if form.validate_on_submit():
        meta = Meta(
            titulo=form.titulo.data.strip(),
            valor_alvo=form.valor_alvo.data,
            valor_atual=form.valor_atual.data or 0,
            prazo=form.prazo.data,
            organizacao_id=current_user.organizacao_id
        )

        db.session.add(meta)
        db.session.commit()

        registrar_auditoria(current_user.id, current_user.organizacao_id, "META_CRIADA", meta.titulo)

        flash("Meta criada.", "success")
        return redirect(url_for("metas.listar"))

    metas = Meta.query.filter_by(organizacao_id=current_user.organizacao_id).order_by(Meta.criado_em.desc()).all()

    return render_template("metas/listar.html", metas=metas, form=form)


@metas_bp.route("/excluir/<int:id>", methods=["POST"])
@login_required
def excluir(id):
    meta = Meta.query.filter_by(id=id, organizacao_id=current_user.organizacao_id).first_or_404()
    titulo = meta.titulo

    db.session.delete(meta)
    db.session.commit()

    registrar_auditoria(current_user.id, current_user.organizacao_id, "META_EXCLUIDA", titulo)

    flash("Meta excluída.", "success")
    return redirect(url_for("metas.listar"))
