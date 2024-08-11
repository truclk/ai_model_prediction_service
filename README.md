# ai_model_prediction_service


# Run server
Ubuntu
Install dependencies

```
sudo apt install python3-pip python3.12-venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
sudo apt install redis-server
```
Prepare database


```
make migrate
```

Edit the `c.IdentityProvider.token` in in `jupyter_notebook_config.py` for security reason


Run server

```
make run_notebook
make run_server
make run_celery
```


