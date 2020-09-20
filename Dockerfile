FROM python:3.7
RUN mkdir -p /tmp/src
COPY . /tmp/src
WORKDIR /tmp/src
RUN pip install -r ./requirements.txt

RUN chmod a+x /tmp/src/entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]