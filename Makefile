alembic init -t async migrations


alembic revision --autogenerate -m <message>

alembic upgrade head

reset_database: alembic stamp head
