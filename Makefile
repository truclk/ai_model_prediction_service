VENV_ACTIVATE := source ./venv/bin/activate


.PHONY: run_notebook run_server run_celery

migrate:
	$(VENV_ACTIVATE) && \
	export JUPYTER_SERVER=127.0.0.1:8888 && \
	export JUPYTER_TOKEN=$$(grep -oP 'c.IdentityProvider.token = "\K[^"]+' jupyter_notebook_config.py) && \
	./manage.py migrate

run_notebook:
	$(VENV_ACTIVATE) && \
	jupyter notebook --NotebookApp.token=$$JUPYTER_TOKEN --config=jupyter_notebook_config.py
run_server:
	$(VENV_ACTIVATE) && \
	export JUPYTER_SERVER=127.0.0.1:8888 && \
	export JUPYTER_TOKEN=$$(grep -oP 'c.IdentityProvider.token = "\K[^"]+' jupyter_notebook_config.py) && \
	./manage.py runserver

run_server_prod:
	$(VENV_ACTIVATE) && \
	export JUPYTER_SERVER=127.0.0.1:8888 && \
	export JUPYTER_TOKEN=$$(grep -oP 'c.IdentityProvider.token = "\K[^"]+' jupyter_notebook_config.py) && \
	./manage.py runserver 0.0.0.0:80

run_celery:
	$(VENV_ACTIVATE) && \
	export JUPYTER_SERVER=127.0.0.1:8888 && \
	export JUPYTER_TOKEN=$$(grep -oP 'c.IdentityProvider.token = "\K[^"]+' jupyter_notebook_config.py) && \
	celery -A ai_model_prediction_service worker -l INFO
