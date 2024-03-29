# Fastapi Template

# init

python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt

pip freeze > requirements.txt

# install and run

pip install -r requirements.txt

# Ejecutar local
uvicorn app.main:app --reload
# Ejecutar con logs nivel INFO
uvicorn app.main:app --log-level info


#### migraciones ####

Crear carpeta "versions" en la ruta ./alembic/

## Comando para generar migraciones cuando se crean o modifican modelos 

alembic revision --autogenerate -m "init"

-------------
alembic revision -m "create table user"
alembic history
alembic current


# Comando para aplicar migraciones en la DB

alembic upgrade head



# Retroceder Migraciones
alembic downgrade -1
alembic downgrade <revision_id>
alembic downgrade base



# Pip update 

pur -r requirements.txt -o updates.txt > update.txt