#!/user/bin python
# -*- coding: utf-8 -*-
#@author:z
#@time:2018-04-12
# import getItemsApi
import config as cfg
import pymysql
import threading
from getItemsApi import GetItemApi
import time
import datetime
import os
import sys
os.chdir(sys.path[0])
import warnings
warnings.filterwarnings("ignore")


class GetItems:
	
	def __init__(self):
		self.keywords = ''
		self.start_time = ''
		self.sleep_time = 0.00
		
	# 获取keywords列表
	def getKeyWords(self,sleep_time):
		self.sleep_time = sleep_time
		conn = pymysql.connect(host=cfg.dbhost,port=cfg.dbport,user=cfg.dbuser,passwd=cfg.dbpass,db=cfg.dbname,charset='utf8')
		cursor = conn.cursor()
		sql = 'SELECT catid,keywords,start_price,end_price,step_size FROM z_tbcates WHERE status = 1'
		try:
			cursor.execute(sql)
			keywordsInfo = cursor.fetchall()
			self.spider_keyword(keywordsInfo)
		except Exception as e:
			print str(e)
		finally:
			cursor.close()
			conn.close()
	
	def spider_keyword(self,keywordsInfo):
		
		try:
			threads = []
			for keywordInfo in keywordsInfo:
				catid = int(keywordInfo[0])
				keywords = keywordInfo[1]
				start_price = int(keywordInfo[2])
				end_price = int(keywordInfo[3])
				step_size = int(keywordInfo[4])
				keywordList = keywords.split(',')
				for keyword in keywordList:
					# 传入采集方法 创建线程
					q = str(keyword.encode('utf-8'))
					api = GetItemApi()
					thread = threading.Thread(name = 'Thread-' + q, target = api.make_steps, args = (q, catid, start_price, end_price, step_size,self.sleep_time))
					threads.append(thread)
			for t in threads:
				t.start()
				# t.join()
		except Exception,e:
			print str(e) + ' 1'

def start ():
	while True:
		try:
			conn = pymysql.connect (host = cfg.dbhost, port = cfg.dbport, user = cfg.dbuser, passwd = cfg.dbpass,
			                        db = cfg.dbname, charset = 'utf8')
			cursor = conn.cursor ()
			sql = 'select `start_time`,`sleep_time` from `z_timeconfig` limit 1'
			cursor.execute(sql)
			res = cursor.fetchone()
			start_time = str(res[0])
			sleep_time = float(res[1])
			start_h = int(start_time.split(':')[0])
			start_m = int(start_time.split(':')[1])
			now = datetime.datetime.now()
			h = int(now.hour)
			m = int(now.minute)
			# GetItems ().getKeyWords (sleep_time)
			if start_h == h and start_m == m:
				print 'start'
				GetItems ().getKeyWords (sleep_time)
			else:
				print 'not now'
				time.sleep(10)
		except Exception,e:
			print str(e)


if __name__ == '__main__':
	start ()
