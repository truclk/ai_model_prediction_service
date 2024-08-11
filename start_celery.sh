export JUPYTER_SERVER=127.0.0.1:8888

# Extract and set the Jupyter token
export JUPYTER_TOKEN=$(grep -oP 'c.IdentityProvider.token = "\K[^"]+' jupyter_notebook_config.py)

# Start Celery
celery -A ai_model_prediction_service worker -l INFO


