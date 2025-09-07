# Executa a migração do banco de dados
flask db upgrade

# Inicia o servidor Gunicorn
gunicorn src.wsgi:app