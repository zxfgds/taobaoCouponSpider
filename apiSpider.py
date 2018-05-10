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
import os
import sys
os.chdir(sys.path[0])
import warnings
warnings.filterwarnings("ignore")


class GetItems:
	
	def __init__(self):
		self.keywords = ''
		self.appKeyList = cfg.appKeyList
	
	# 获取keywords列表
	def getKeyWords(self):
		conn = pymysql.connect(host=cfg.dbhost,port=cfg.dbport,user=cfg.dbuser,passwd=cfg.dbpass,db=cfg.dbname,charset='utf8')
		cursor = conn.cursor()
		sql = 'SELECT catid,keywords,start_price,end_price,step_size FROM shz_tbcates WHERE status = 1'
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
					thread = threading.Thread(name = 'Thread-' + q,target = api.make_steps,args = (q,catid,start_price,end_price,step_size) )
					threads.append(thread)
			for t in threads:
				t.start()
		except Exception,e:
			print str(e) +  ' 1'


def start ():
	while True:
		GetItems ().getKeyWords ()
		time.sleep (86400)


if __name__ == '__main__':
	start ()

	