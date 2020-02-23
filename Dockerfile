FROM python:3-alpine

WORKDIR /pt-issuesapp
COPY ./dist/pt_test_issuesapp-*.whl .

RUN pip install --upgrade pip
RUN pip install pt_test_issuesapp-*.whl

ENTRYPOINT [ "pt-test-issuesapp" ]
