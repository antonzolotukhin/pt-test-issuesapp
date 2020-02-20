FROM python:3-alpine

WORKDIR /pt-issuesapp
COPY requirements.txt .
COPY issuesapp.py .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD [ "python", "./issuesapp.py" ]
