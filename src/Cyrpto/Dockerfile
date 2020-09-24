FROM python:3

RUN pip install pycoingecko flask requests flask_bootstrap gunicorn

ADD __init__.py __init__.py
ADD Application.py Application.py
ADD coin.py coin.py
ADD recent_history.py recent_history.py
ADD crypto_api.py crypto_api.py
ADD start.sh start.sh
ADD wsgi.py wsgi.py 


CMD python3 Application.py & gunicorn -b 0.0.0.0:5001 wsgi:app
