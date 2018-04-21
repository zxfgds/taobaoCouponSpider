#!/user/bin python
# -*- coding: utf-8 -*-
#@author:z
#@time:2018-04-12
import top.api
import config as cfg
import random
import pymysql
import time

class CheckCoupon:
	
	def __init__ (self):
		self.app_key_secret = cfg.appKeyList[random.randint (0, len (cfg.appKeyList) - 1)]
	
	def getAppKey (self):
		conn = pymysql.connect (host = cfg.dbhost, port = cfg.dbport, user = cfg.dbuser, passwd = cfg.dbpass,
		                        db = cfg.dbname, charset = 'utf8')
		cur = conn.cursor ()
		sql = 'SELECT `key`, `secret`, `adzoneid` FROM shz_appkey  WHERE ban_time < %d  order by RAND() limit 1' % int (
			time.time ())
		try:
			cur.execute (sql)
			r = cur.fetchone ()
			return r
		except Exception, e:
			print str (e) + '???'
		finally:
			cur.close ()
			conn.close ()

	# 查询优惠券信息
	
	def check_coupon_info (self, num_iid, activity_id):
		app_key_secret = self.getAppKey ()
		appkey = int (app_key_secret[0])
		secret = str (app_key_secret[1])
		req = top.api.TbkCouponGetRequest ()
		req.set_app_info (top.appinfo (appkey, secret))
		req.item_id = num_iid
		req.activity_id = activity_id
		try:
			resp = req.getResponse ()
			return resp['tbk_coupon_get_response']['data']
		except Exception, e:
			print(e)  + '   6'