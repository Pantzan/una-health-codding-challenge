start_containers:
	DOCKER_BUILDKIT=1 docker compose up -d --build

stop_containers:
	DOCKER_BUILDKIT=1 docker compose down --remove-orphans

logs_server:
	docker compose logs una-health-app -f

load_initial_data_docker:
	docker compose exec una-health-app python manage.py loaddata fixtures/user.json

migrate_docker:
	docker compose exec una-health-app python manage.py migrate --noinput

run_tests_docker:
	docker compose exec una-health-app pytest -v

migrate:
	python manage.py migrate --noinput

load_initial_data:
	python manage.py loaddata fixtures/user.json

run_server:
	docker compose up db -d
	python manage.py runserver 0.0.0.0:8000

run_tests:
	pytest -v

push_metrics_data_docker:
	docker compose exec una-health-app curl -X POST 127.0.0.1:8000/api/v1/create_report/ \
		--form report_file="@sample_data/aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa.csv" -v
