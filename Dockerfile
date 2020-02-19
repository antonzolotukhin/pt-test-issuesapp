FROM python:3

ADD issuesapp.py /

RUN pip install -r requirements.txt

CMD [ "python", "./issuesapp.py" ]
