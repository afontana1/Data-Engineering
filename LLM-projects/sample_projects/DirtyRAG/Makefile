.PHONY: check_env create_env activate_venv run_postgres

check_env:
	@if [ ! -d "env" ]; then \
		echo "Run ./scripts/create_env to build the env"; \
	else \
		echo "env directory already exists."; \
	fi

create_env:
	@if [ ! -d "env" ]; then \
		python3.10 -m venv env && \
		echo "Virtual environment created in 'env' directory."; \
	fi

activate_venv:
	@source env/bin/activate && \
	echo "Virtual environment activated." && \
	which python | grep 'env' && \
	echo "Virtual environment has been validated and activated!" || \
	echo "Activation failed."

deactivate_venv:
	@echo "To deactivate the virtual environment, run:"
	deactivate

install_requirements:
	@echo "Installing requirements from requirements.txt..."
	pip install -r requirements.txt

update_pip: activate_venv
	pip install --upgrade pip

save_deps: activate_venv
	pip freeze > requirements.txt

run_postgres:
	@echo "Starting Postgres on :5001"
	@docker-compose -f docker/postgres-docker-compose.yml up

