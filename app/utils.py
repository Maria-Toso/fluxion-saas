from app.extensions import db
from app.models import Auditoria


def registrar_auditoria(usuario_id, organizacao_id, acao, detalhes=None):
    log = Auditoria(
        usuario_id=usuario_id,
        organizacao_id=organizacao_id,
        acao=acao,
        detalhes=detalhes
    )

    db.session.add(log)
    db.session.commit()
