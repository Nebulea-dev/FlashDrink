# What is this backend

# What are the routes of the backend

# How to run this backend

1) Install `UV`
```
curl -LsSf https://astral.sh/uv/install.sh | sh
```

2) Create a venv

```
uv venv
```

3) Install dependencies

```uv pip sync requirements.txt```

4) Run the backend

```
source .venv/bin/activate
.venv/bin/gunicorn --workers 4 --bind 0.0.0.0:5000 app:app
```

5) (Optional) Add backend as a linux service with systemctl

Put the following (and modify as needed) in `/etc/systemd/system/flask-drink-payment.service` :

```
[Unit]
Description=Flask Drink Payment System
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/objetconnecte
ExecStart=/home/ubuntu/objetconnecte/.venv/bin/gunicorn --workers 4 --bind 0.0.0.0:5000 app:app
Restart=always
Environment="PATH=/home/ubuntu/objetconnecte/.venv/bin"
Environment="PYTHONUNBUFFERED=1"

[Install]
WantedBy=multi-user.target
```

Then, restart services with `sudo systemctl daemon-reload`
