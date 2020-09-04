FROM python:3

RUN pip install pycoingecko flask

ADD __init__.py __init__.py
ADD Application.py Application.py
ADD coin.py coin.py
ADD recent_history.py recent_history.py
ADD crypto_api.py crypto_api.py

EXPOSE 5001

CMD [ "python3", "./Application.py" ]
CMD [ "python3", "./crypto_api.py"]
