FROM python:buster

WORKDIR /app

COPY . /app

RUN pip3 install -i https://pypi.douban.com/simple lxml requests tqdm pymysql faunadb pymongo

CMD python weibo.py
