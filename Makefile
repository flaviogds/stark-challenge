# Application
run:
	fastapi dev --host 0.0.0.0 --port=80 --reload ./src/main.py
test:
	coverage run

test-coverage:
	coverage report

coverage-browser:
	 coverage html && cd htmlcov && python -m webbrowser index.html && cd ..

lint:
	pylint --recursive=y app/ tests/

format:
	pyink -q . && isort .

security-checks:
	bandit -c pyproject.toml -r app

# Docker Utils
docker-start:
	docker-compose up -d --build

docker-stop:
	docker-compose down --remove-orphans

docker-logs:
	 docker-compose logs -f app

DOKCER_EXEC=docker-compose exec app

docker-shell:
	$(DOCKER_EXEC) bash

docker-test:
	$(DOCKER_EXEC) make test

docker-test-coverage:
	$(DOCKER_EXEC) sh -c make test-coverage
