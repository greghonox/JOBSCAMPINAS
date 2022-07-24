create-venv:
	python3 -m venv venv

activate-venv:
	source venv/bin/activate

install-requirements:
	venv/bin/pip install -r requirements.txt

pip-freeze:
	venv/bin/pip freeze