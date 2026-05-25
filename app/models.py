from datetime import datetime, date
from flask_login import UserMixin
from app.extensions import db


class Organizacao(db.Model):
    __tablename__ = "organizacoes"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(140), nullable=False)
    plano = db.Column(db.String(40), nullable=False, default="free")
    status = db.Column(db.String(40), nullable=False, default="active")
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

    usuarios = db.relationship("Usuario", backref="organizacao", lazy=True, cascade="all, delete-orphan")
    categorias = db.relationship("Categoria", backref="organizacao", lazy=True, cascade="all, delete-orphan")
    transacoes = db.relationship("Transacao", backref="organizacao", lazy=True, cascade="all, delete-orphan")
    metas = db.relationship("Meta", backref="organizacao", lazy=True, cascade="all, delete-orphan")


class Usuario(db.Model, UserMixin):
    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(180), unique=True, nullable=False, index=True)
    senha = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(30), nullable=False, default="owner")
    ativo = db.Column(db.Boolean, default=True)
    ultimo_login = db.Column(db.DateTime, nullable=True)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

    organizacao_id = db.Column(db.Integer, db.ForeignKey("organizacoes.id"), nullable=False)


class Categoria(db.Model):
    __tablename__ = "categorias"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), nullable=False)
    tipo = db.Column(db.String(20), nullable=False)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

    organizacao_id = db.Column(db.Integer, db.ForeignKey("organizacoes.id"), nullable=False)

    transacoes = db.relationship("Transacao", backref="categoria", lazy=True)


class Transacao(db.Model):
    __tablename__ = "transacoes"

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(120), nullable=False)
    valor = db.Column(db.Float, nullable=False)
    tipo = db.Column(db.String(20), nullable=False)
    data = db.Column(db.Date, nullable=False, default=date.today)
    observacao = db.Column(db.Text, nullable=True)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

    organizacao_id = db.Column(db.Integer, db.ForeignKey("organizacoes.id"), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)
    categoria_id = db.Column(db.Integer, db.ForeignKey("categorias.id"), nullable=True)

    usuario = db.relationship("Usuario", backref="transacoes")


class Meta(db.Model):
    __tablename__ = "metas"

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(120), nullable=False)
    valor_alvo = db.Column(db.Float, nullable=False)
    valor_atual = db.Column(db.Float, nullable=False, default=0)
    prazo = db.Column(db.Date, nullable=True)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

    organizacao_id = db.Column(db.Integer, db.ForeignKey("organizacoes.id"), nullable=False)

    @property
    def progresso(self):
        if self.valor_alvo <= 0:
            return 0
        return min(100, round((self.valor_atual / self.valor_alvo) * 100, 1))


class Auditoria(db.Model):
    __tablename__ = "auditoria"

    id = db.Column(db.Integer, primary_key=True)
    acao = db.Column(db.String(160), nullable=False)
    detalhes = db.Column(db.Text, nullable=True)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

    usuario_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=True)
    organizacao_id = db.Column(db.Integer, db.ForeignKey("organizacoes.id"), nullable=False)

    usuario = db.relationship("Usuario", backref="auditorias")
