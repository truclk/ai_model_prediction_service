.PHONY: run

run_notebook:
	jupyter notebook --NotebookApp.token=$$JUPYTER_TOKEN --config=jupyter_notebook_config.py
run_server:
	export JUPYTER_SERVER=127.0.0.1:8888 && \
	export JUPYTER_TOKEN=$$(grep -oP 'c.IdentityProvider.token = "\K[^"]+' jupyter_notebook_config.py) && \
	./manage.py runserver
run_celery:
	export JUPYTER_SERVER=127.0.0.1:8888 && \
	export JUPYTER_TOKEN=$$(grep -oP 'c.IdentityProvider.token = "\K[^"]+' jupyter_notebook_config.py) && \
	celery -A ai_model_prediction_service worker -l INFO
