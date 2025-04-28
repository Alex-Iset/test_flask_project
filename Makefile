install:
	uv sync

# Запуск приложения локально (в режиме отладки)
start:
	uv run flask --app example --debug run --port 8000

# Запуск приложения через gunicorn (для продакшена)
run:
	uv run gunicorn example:app --bind 0.0.0.0:$PORT

lint:
	uv run ruff check

lint-fix:
	uv run ruff check --fix
