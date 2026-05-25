# Fluxion SaaS

Fluxion é um sistema financeiro em formato SaaS, feito com Flask, SQLAlchemy, Flask-Login, Flask-WTF, Flask-Limiter, TailwindCSS e Chart.js.

## Funcionalidades

- Cadastro e login com senha criptografada
- Multi-tenant por organização
- Roles: owner, admin e member
- Dashboard financeiro
- CRUD de transações
- Categorias por organização
- Metas financeiras
- Relatórios com gráficos
- Auditoria de ações importantes
- Painel administrativo básico
- CSRF em formulários
- Rate limit em login/cadastro
- Headers de segurança
- Cookies seguros configuráveis
- Pronto para SQLite local ou PostgreSQL em produção

## Rodar localmente

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python run.py
```

Acesse:

```txt
http://127.0.0.1:5000
```

## Deploy

Para Render/Railway/Fly.io:

```txt
Build Command: pip install -r requirements.txt
Start Command: gunicorn run:app
```

Configure as variáveis:

```txt
SECRET_KEY=<chave forte>
DATABASE_URL=<url do postgres ou sqlite>
SECURE_COOKIES=true
```

## Segurança

Este projeto já inclui boas práticas, mas nenhum app é "100% seguro". Antes de usar com dinheiro real:
- use HTTPS
- use PostgreSQL
- configure backups
- rode testes
- revise permissões
- monitore logs
- faça auditoria externa
=======
# fluxion-saas
>>>>>>> 66388ba1f05e11d4a753f732fd09aae067f7832a
