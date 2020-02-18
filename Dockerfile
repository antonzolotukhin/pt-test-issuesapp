FROM python:3

ADD issuesapp.py /

RUN pip install requests

CMD [ "python", "./issuesapp.py" ]
