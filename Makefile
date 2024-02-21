mm:
	alembic revision --autogenerate
	alembic upgrade heads

run:
	python3 main.py