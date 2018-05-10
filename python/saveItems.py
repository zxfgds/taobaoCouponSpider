#!/user/bin python
# -*- coding: utf-8 -*-
#@author:z
#@time:2018-04-12
import pymongo
import pymysql
import config as cfg
from checkCoupon import CheckCoupon
import os
import sys
os.chdir(sys.path[0])
import warnings
# warnings.filterwarnings("ignore")

class SaveItems:
	def __init__(self):
		pass

	def checkExists(self,keyword,items,catid):
		conn = pymongo.MongoClient('127.0.0.1',27017)
		db = conn.taobao
		collections = db.itemsLog
		
		try:
			itemDictList = []
			insertSql = 'INSERT IGNORE INTO z_items (' \
					'`num_iid`,`title`,`pict_url`,`provcity`,`commission_type`,`small_images`,' \
					'`user_type`,`tk_total_sales`,`coupon_info`,`item_url`,`commission_rate`,`coupon_total_count`,' \
					'`include_mkt`,`include_dxjh`,`tk_total_commi`,`zk_final_price`,`shop_title`,`volume`,' \
					'`coupon_id`,`coupon_value`,`coupon_start_fee`,`coupon_remain_count`,`coupon_start_time`,`coupon_end_time`,' \
					'`seller_id`,`free_shipment`,`qqhd`,`tao_ke_price`,`category`,`commission`' \
					') VALUES  '
			for item in items:
				check = collections.find_one({'num_iid':item['num_iid']})
				# 优惠券信息
				couponInfo = CheckCoupon ().check_coupon_info (item['num_iid'], item['coupon_id'])
				# # 实际价格
				tao_ke_price = float (item['zk_final_price']) - float (couponInfo['coupon_amount'])
				if tao_ke_price < 0:
					continue

				# 佣金
				commission = int(item['commission_rate']) * float(item['zk_final_price']) / 10000
				
				# 是否有小图
				if 'small_images' in item:
					small_images = ''
					for image in item['small_images']['string']:
						small_images += image.encode('utf-8')
				else:
					small_images = ''

				if str (item['include_mkt'].encode ('utf-8')) == 'true':
					item['include_mkt'] = 1
				else:
					item['include_mkt'] = 0

				if str (item['include_dxjh'].encode ('utf-8')) == 'true':
					item['include_dxjh'] = 1
				else:
					item['include_dxjh'] = 0

				itemDict = {
					'num_iid': item['num_iid'],  # 商品ID
					'title': item['title'],  # 商品名称
					'pict_url': item['pict_url'],  # 主图链接
					'provcity': item['provcity'],  # 发货地
					'commission_type': item['commission_type'],  # 类型
					'small_images': small_images,  # 小图
					'user_type': item['user_type'],  # 用户类型 0 集市 1 天猫
					'tk_total_sales': item['tk_total_sales'],  # 淘客推广数量
					'coupon_info': item['coupon_info'],  # 优惠券信息
					'item_url': item['item_url'],  # 商品链接
					'commission':commission,     # 佣金
					'commission_rate': item['commission_rate'],  # 淘客佣金率   除100
					'coupon_total_count': item['coupon_total_count'],  # 优惠券数量
					'include_mkt': item['include_mkt'],  # 包含是否包含营销计划
					'include_dxjh': item['include_dxjh'],  # 包含定向计划
					'tk_total_commi': item['tk_total_commi'],  # 30天支出总佣金
					'zk_final_price': item['zk_final_price'],  # 真实价格
					'shop_title': item['shop_title'],  # 商铺名称
					'volume': item['volume'],  # 30天销量
					'coupon_id': item['coupon_id'],  # 优惠券ID
					'coupon_value': couponInfo['coupon_amount'],  # 优惠券面额
					'coupon_start_fee': couponInfo['coupon_start_fee'],  # 优惠券适用价格
					'coupon_remain_count': item['coupon_remain_count'],  # 优惠券剩余量
					'coupon_start_time': item['coupon_start_time'],  # 优惠开始时间
					'coupon_end_time': item['coupon_end_time'],  # 优惠结束时间
					'seller_id': item['seller_id'],  # 卖家ID
					'free_shipment': 0,  # 包邮信息
					'qqhd': 0,  # 高佣信息
					'tao_ke_price': tao_ke_price,  # 最终价格(减掉优惠券)
					'category': catid
				}

				insertOneSql = \
					'(' \
					'%d,"%s","%s","%s","%s","%s",' \
					'%d,%d,"%s","%s","%s",%d,' \
					'%d,%d,"%s","%s","%s",%d,' \
					'"%s","%s","%s",%d,"%s","%s",' \
					'%d,%d,%d,"%s",%d,"%s"' \
					'),' % (
						int (item['num_iid']), str (item['title'].encode ('utf-8')),
						str (item['pict_url'].encode ('utf-8')), str (item['provcity'].encode ('utf-8')),
						str (item['commission_type'].encode ('utf-8')), small_images,
						int (item['user_type']), int (item['tk_total_sales']),
						str (item['coupon_info'].encode ('utf-8')), str (item['item_url'].encode ('utf-8')),
						int (item['commission_rate']) / 100,
						int (item['coupon_total_count']),
						item['include_mkt'], item['include_dxjh'],
						str (item['tk_total_commi'].encode ('utf-8')),
						str (item['zk_final_price'].encode ('utf-8')), str (item['shop_title'].encode ('utf-8')),
						int (item['volume']),
						str (item['coupon_id'].encode ('utf-8')),
						str (couponInfo['coupon_amount'].encode ('utf-8')),
						str (couponInfo['coupon_start_fee'].encode ('utf-8')),
						int (item['coupon_remain_count']),
						str (item['coupon_start_time'].encode ('utf-8')),
						str (item['coupon_end_time'].encode ('utf-8')),
						int (item['seller_id']), 0, 0, tao_ke_price, int (catid),str(commission)
					)

				if check == None:

					itemDictList.append (itemDict)
					insertSql += insertOneSql

				# 价格有变化
				elif check['tao_ke_price'] != tao_ke_price:
					self.updateMongoLog(item['num_iid'],itemDict)
					# 更新太麻烦  直接删除重建
					self.saveToMysql('DELETE FROM shz_item_info where num_iid = %d') % int (item['num_iid'])
					sql = 'INSERT IGNORE INTO shz_item_info (' \
					'`num_iid`,`title`,`pict_url`,`provcity`,`commission_type`,`small_images`,' \
					'`user_type`,`tk_total_sales`,`coupon_info`,`item_url`,`commission_rate`,`coupon_total_count`,' \
					'`include_mkt`,`include_dxjh`,`tk_total_commi`,`zk_final_price`,`shop_title`,`volume`,' \
					'`coupon_id`,`coupon_value`,`coupon_start_fee`,`coupon_remain_count`,`coupon_start_time`,`coupon_end_time`,' \
					'`seller_id`,`free_shipment`,`qqhd`,`tao_ke_price`,`category`,`commission`' \
					') VALUES  ' + insertOneSql
					self.saveToMysql(sql[:-1])
				else:
					# print  keyword.decode ('utf-8') + u'   \036[1;36m Insert : \036[0m' + str(item['num_iid'])
					pass
			# with open(str(round(time.time()*1000)) +'.txt','w') as insertSqlTxt:
			# 	insertSqlTxt.write(insertSql)
			# 保存日志 新品
			# Update FreeShipment/qqHd: \033[0m'

			if len(itemDictList) > 0:
				print  keyword.decode('utf-8')   + u'   \033[1;36m Insert : \033[0m' + str(len(itemDictList))
				self.saveToMongoLog(itemDictList)
				self.saveToMysql(insertSql[:-1])
			else:
				pass
		except Exception as e:
			# pass
			print str(e) + '   checkExists'
		finally:
			pass

	# 保存到日志
	def saveToMongoLog(self,itemDictList):
		conn = pymongo.MongoClient('127.0.0.1',27017)
		db = conn.taobao
		colLog = db.itemsLog
		colItem = db.itemsNew
		try:
			colLog.insert_many(itemDictList)
			# colItem.insert_many(itemDictList)
		except Exception,e:
			pass
			# print str(e) + '   saveToMongoLog'
	
	
	# 更新产品
	def updateMongoLog(self, num_iid, upDict):
		conn = pymongo.MongoClient('127.0.0.1',27017)
		db = conn.taobao
		colLog = db.itemsLog
		try:
			colLog.update({'num_iid': num_iid}, upDict)
		except Exception,e:
			pass
			# print str(e) + '  updateMongoLog'
	
	
	# 保存到Mysql
	def saveToMysql(self, sql):
		conn = pymysql.connect(host=cfg.dbhost,port=cfg.dbport,user=cfg.dbuser,passwd=cfg.dbpass,db=cfg.dbname,charset='utf8')
		conn.autocommit (1)
		cur = conn.cursor()
		try:
			conn.begin()
			cur.execute(sql)
			conn.commit()
		except Exception,e:
			pass
			# print str(e) + ' saveToMysql'
		finally:
			cur.close()
			conn.close()