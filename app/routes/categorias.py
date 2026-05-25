from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app.extensions import db
from app.models import Categoria
from app.forms import CategoriaForm
from app.utils import registrar_auditoria

categorias_bp = Blueprint("categorias", __name__, url_prefix="/categorias")


@categorias_bp.route("/", methods=["GET", "POST"])
@login_required
def listar():
    form = CategoriaForm()

    if form.validate_on_submit():
        categoria = Categoria(
            nome=form.nome.data.strip(),
            tipo=form.tipo.data,
            organizacao_id=current_user.organizacao_id
        )

        db.session.add(categoria)
        db.session.commit()

        registrar_auditoria(current_user.id, current_user.organizacao_id, "CATEGORIA_CRIADA", categoria.nome)

        flash("Categoria criada.", "success")
        return redirect(url_for("categorias.listar"))

    categorias = Categoria.query.filter_by(organizacao_id=current_user.organizacao_id).order_by(Categoria.nome).all()

    return render_template("categorias/listar.html", categorias=categorias, form=form)


@categorias_bp.route("/excluir/<int:id>", methods=["POST"])
@login_required
def excluir(id):
    categoria = Categoria.query.filter_by(id=id, organizacao_id=current_user.organizacao_id).first_or_404()
    nome = categoria.nome

    db.session.delete(categoria)
    db.session.commit()

    registrar_auditoria(current_user.id, current_user.organizacao_id, "CATEGORIA_EXCLUIDA", nome)

    flash("Categoria excluída.", "success")
    return redirect(url_for("categorias.listar"))
