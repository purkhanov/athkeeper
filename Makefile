run:
	uvicorn src.main:app --reload


alembic_init:
	alembic init -t async migrations

alembic_revision:
	alembic revision --autogenerate -m "Initial tables"


alembic_up_head:
	alembic upgrade head
