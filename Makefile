.PHONY: run

run:
	export JUPYTER_TOKEN=$$(openssl rand -hex 32) && \
	echo "export JUPYTER_TOKEN=$$JUPYTER_TOKEN" && \
	(jupyter notebook --NotebookApp.token=$$JUPYTER_TOKEN --config=jupyter_notebook_config.py &) && \
	./manage.py runserver
run_server:
	./manage.py runserver
run_celery:
	celery -A ai_model_prediction_service worker -l INFO
