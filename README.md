# Proyecto FastAPI para la App Móvil de Selene

Este repositorio contiene el código fuente para una aplicación móvil desarrollada con FastAPI, diseñada especialmente para el cumpleaños número 15 de Selene.

## Descripción del Proyecto

La aplicación móvil está destinada a proporcionar una experiencia interactiva y emocionante para los invitados al evento de cumpleaños de Selene. Contiene varias características clave, incluyendo:

- **Registro de Invitados**: Los invitados pueden registrarse en la aplicación, proporcionando su nombre y detalles de contacto.
- **Información del Evento**: Información detallada sobre la fecha, hora, ubicación y actividades planificadas para el cumpleaños de Selene.
- **Posts del evento**: Red social temporal donde invitdos pueden subir contenido multimedia y opinar sobre ellos.
- **Notificaciones**: Funcionalidad de mensajería integrada para que los invitados puedan recibir información sobre el evento.

## Tecnologías Utilizadas

El proyecto se desarrolla utilizando las siguientes tecnologías principales:

- **FastAPI**: Un moderno marco de desarrollo web para crear APIs rápidas con Python.
- **Postgresql**: Una base de datos relacional ligera que se utiliza para almacenar los datos de la aplicación.


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


## Licencia

Este proyecto está bajo la licencia MIT.

---
**Nota:** Este proyecto es una iniciativa para celebrar el cumpleaños de Selene y no tiene fines comerciales. Todos los derechos de autor y créditos de las imágenes utilizadas en la aplicación corresponden a sus respectivos propietarios.
