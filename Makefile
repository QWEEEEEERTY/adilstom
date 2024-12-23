init_db:
	alembic init -t async migrations

revision:
	alembic revision --autogenerate -m "first revision"

migrate:
	alembic upgrade head

reset_database:
	alembic stamp head

run:
	gunicorn -w 1 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000 src.main:app

reset:
	docker-compose down --rmi all --volumes --remove-orphans
