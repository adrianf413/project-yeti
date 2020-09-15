FROM python:3

RUN pip install pycoingecko flask requests flask_bootstrap gunicorn

ADD /img /img
ADD /static /static
ADD /templates /templates
ADD coin.py coin.py 
ADD yeti_frontend.py yeti_frontend.py 

EXPOSE 5002

CMD gunicorn -b 0.0.0.0:5012 yeti_frontend:app
