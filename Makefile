install:
	uv sync

collectstatic:
	uv run python manage.py collectstatic --no-input

migrations:
	uv run python manage.py makemigrations
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

test:
	uv run python manage.py test

tree:
	tree -I __pycache__ -I staticfiles