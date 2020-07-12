# AppFollow
Тестовое задание от AppFollow

Добавить директорию backend/app
Скопировать файл pyproject.toml, удалить лишние зависимости
Скопировать backend.dockerfile, удалить Jupyter
Скопировать docker-compose.yml

docker-compose exec db psql -U postgres
\password postgres
!!! Так должно быть?

Раскомментировать строку
command: bash -c "while true; do sleep 1; done"  # Infinite loop to keep container live doing nothing
в docker-compose.override.yml

Автоматически инициализировать таблицы
alembic revision --autogenerate -m "baseline"

Снова закомментировать строку в docker-compose.override.yml

docker-compose up -d

Тестирование в git-bash
export MSYS_NO_PATHCONV=1 ./scripts/test.sh


// Frontend, built with Docker, with routes handled based on the path: http://localhost

Backend, JSON based web API based on OpenAPI: http://localhost/api/

Automatic interactive documentation with Swagger UI (from the OpenAPI backend): http://localhost/docs

Alternative automatic documentation with ReDoc (from the OpenAPI backend): http://localhost/redoc

PGAdmin, PostgreSQL web administration: http://localhost:5050

Flower, administration of Celery tasks: http://localhost:5555

Traefik UI, to see how the routes are being handled by the proxy: http://localhost:8090
