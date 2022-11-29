.PHONY: interactive build ugc services
ugc: build-dockers-ugc

.PHONY: clean all docker images and pyc-files
clean-all: clean-pyc clean-all-dockers

.PHONY: run pre-commit all files
pre-commit: create-venv pip-install-pre-commit pre-commit-files

.PHONY: create venv
create-venv:
	python3 -m venv venv

.PHONY: install requirements-build to venv
pip-install-build:
	./venv/bin/pip3 install -r requirements-build.txt

.PHONY: install requirements-pre-commit to venv
pip-install-pre-commit:
	./venv/bin/pip3 install -r requirements-pre-commit.txt

.PHONY: interactive build docker services
build-dockers:
	docker-compose --profile dev up --build

.PHONY: interactive build docker ugc services 
build-dockers-ugc:
	docker-compose --profile dev_ugc up --build

.PHONY: run pre-commit all files
pre-commit-files:
	source venv/bin/activate; ./venv/bin/pre-commit run --all-files

.PHONY: clean-pyc
clean-pyc:
	find . -type f -name '*.py[co]' -delete -o -type d -name __pycache__ -delete

.PHONY: clean all docker images
clean-all-dockers:
	T=$$(docker ps -q); docker stop $$T; docker rm $$T; docker container prune -f