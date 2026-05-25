from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.security import roles_required
from app.models import Usuario, Auditoria, Organizacao

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


@admin_bp.route("/")
@login_required
@roles_required("owner", "admin")
def index():
    usuarios = Usuario.query.filter_by(organizacao_id=current_user.organizacao_id).order_by(Usuario.criado_em.desc()).all()
    logs = Auditoria.query.filter_by(organizacao_id=current_user.organizacao_id).order_by(Auditoria.criado_em.desc()).limit(50).all()
    organizacao = Organizacao.query.get(current_user.organizacao_id)

    return render_template("admin/index.html", usuarios=usuarios, logs=logs, organizacao=organizacao)
