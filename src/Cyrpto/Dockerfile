FROM python:3

RUN pip install pycoingecko

ADD __init__.py __init__.py
ADD Application.py Application.py
ADD coin.py coin.py
ADD recent_history.py recent_history.py

CMD [ "python3", "./Application.py" ]
