install:
	uv sync

collectstatic:
	uv run python manage.py collectstatic --no-input

migrate:
	uv run python manage.py migrate

setup: install collectstatic migrate

build:
	./build.sh

render-start:
	uv run gunicorn task_manager.wsgi

start:
	uv run python manage.py runserver

build-assets:
	uv run python manage.py tailwind build
	uv run python manage.py collectstatic --no-input

compilemessages:
	uv run python manage.py compilemessages

tree:
	tree -I __pycache__ -I staticfiles