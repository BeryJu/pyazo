all: lint-fix lint coverage

coverage:
	coverage run --concurrency=multiprocessing manage.py test pyazo --failfast
	coverage combine
	coverage html
	coverage report

lint-fix:
	isort -rc .
	black .

lint:
	pyright
	bandit -r .
	pylint pyazo
	prospector
