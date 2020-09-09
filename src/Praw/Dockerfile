FROM python:3

RUN pip install nltk flask praw

ADD __init__.py __init__.py
ADD main_live.py main_live.py
ADD Reddit_Comments.py Reddit_Comments.py
ADD normalisation.py normalisation.py
ADD classify.py classify.py
ADD configuration.yaml configuration.yaml 
ADD api_praw.py api_praw.py
#ADD TextClassifier/Classifiers

EXPOSE 5003

CMD python3 main_live.py & python3 api_praw.py