#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from loguru import logger
import warnings
import os
import json


class MySQL():
  def __init__(self, config):
    try:
      import pymysql
    except ImportError:
      sys.exit('please check pymysql installed or not')
    self.mysql_connection = pymysql.connect(**config)
    create_table_sql = """
            CREATE TABLE IF NOT EXISTS weibo (
            id varchar(20) NOT NULL,
            bid varchar(12) NOT NULL,
            user_id varchar(20),
            screen_name varchar(20),
            text varchar(2000),
            topics varchar(200),
            at_users varchar(200),
            pics varchar(1000),
            video_url varchar(300),
            location varchar(100),
            created_at DATETIME,
            source varchar(30),
            attitudes_count INT,
            comments_count INT,
            reposts_count INT,
            retweet_id varchar(20),
            PRIMARY KEY (id)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4"""
    self.mysql_execute(create_table_sql)
    create_table = """
            CREATE TABLE IF NOT EXISTS user (
            id varchar(20) NOT NULL,
            screen_name varchar(30),
            gender varchar(10),
            statuses_count INT,
            followers_count INT,
            follow_count INT,
            description varchar(140),
            profile_url varchar(200),
            profile_image_url varchar(200),
            avatar_hd varchar(200),
            urank INT,
            mbrank INT,
            verified BOOLEAN DEFAULT 0,
            verified_type INT,
            verified_reason varchar(140),
            PRIMARY KEY (id)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4"""
    self.execute(create_table)

  def execute(self, sql):
    with warnings.catch_warnings():
      warnings.simplefilter("ignore")
      try:
        with self.mysql_connection.cursor() as cursor:
          cursor.execute(sql)
      except Exception as e:
        print('Error: ', e)
        traceback.print_exc()

  def insert(self, table, data_list):
    if len(data_list) > 0:
      keys = ', '.join(data_list[0].keys())
      values = ', '.join(['%s'] * len(data_list[0]))
      cursor = self.mysql_connection.cursor()
      sql = "INSERT INTO {table}({keys}) VALUES ({values}) ON DUPLICATE KEY UPDATE".format(table=table, keys=keys, values=values)
      update = ','.join([" {key} = values({key})".format(key=key) for key in data_list[0]])
      sql += update
      try:
        cursor.executemany(sql, [tuple(data.values()) for data in data_list])
        self.mysql_connection.commit()
      except Exception as e:
        self.mysql_connection.rollback()
        print('Error: ', e)
        traceback.print_exc()


if __name__ == "__main__":
  config_path = os.path.split(os.path.realpath(__file__))[0] + os.sep + 'config.json'
  if not os.path.isfile(config_path):
    sys.exit(u'当前路径：%s 不存在配置文件config.json' % (os.path.split(os.path.realpath(__file__))[0] + os.sep))
  with open(config_path) as f:
    config = json.loads(f.read())
  MySQL(config['mysql_config'])
