FROM python:3-alpine

WORKDIR /pt-issuesapp
COPY requirements.txt .
COPY ./dist/*.egg .

RUN pip install --upgrade pip
RUN pip install setuptools
RUN pip install -r requirements.txt
RUN easy_install *.egg

ENTRYPOINT [ "pt-test-issuesapp" ]
