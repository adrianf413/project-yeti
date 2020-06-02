FROM python:3

RUN pip install pycoingecko

ADD __init__.py
ADD Application.py
ADD coin.py
ADD recent_histoy.py

CMD [ "python3", "./Application.py" ]
