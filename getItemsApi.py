# -*- coding: utf-8 -*-
'''
Created on 2012-7-3

@author: lihao
'''
import top.api
import config as cfg
import random
from  saveItems import  SaveItems
import time
import os
import sys
import pymysql
os.chdir(sys.path[0])
import warnings
warnings.filterwarnings("ignore")



class GetItemApi:
    
    def __init__(self):
        pass
    
    # 获取商品
    def getItemList(self,page_no,start_step,end_step,keyword,catid):
        app_key_secret = self.getAppKey ()
        appkey = int(app_key_secret[0])
        secret = str(app_key_secret[1])
        req=top.api.TbkDgMaterialOptionalRequest()
        req.set_app_info(top.appinfo(appkey,secret))
        req.start_price = start_step
        req.end_price= end_step
        req.q = keyword
        req.page_no = page_no
        req.cat = catid
        req.adzone_id = int(app_key_secret[2])
        req.page_size=100
        req.platform=2
        req.is_overseas= 'false'
        req.is_tmall= 'false'
        req.has_coupon= 'true'
        try:
            resp= req.getResponse()
            return resp
        except Exception,e:
            if 'errorcode=15' in str(e):
                with(open('errPid.log','a+')) as errPid:
                    errPid.write(str(appkey)+' ' + str(secret) + ' ' + str(app_key_secret[2]) + "\n")
            if 'errorcode=7' in str(e):
                bantime = str(e)[117:].split(' ')[0]
                self.updateBantime(int(app_key_secret[0]),int(bantime))
                return self.getItemList (int(page_no), int(start_step), int(end_step), str(keyword), int(catid))
            else:
                print str(e)  + '???'
                with(open('apiErr.log','a+')) as apiErr:
                    apiErr.write(str(e) +  "\n")

    def getAppKey(self):
        conn = pymysql.connect (host = cfg.dbhost, port = cfg.dbport, user = cfg.dbuser, passwd = cfg.dbpass,
                                db = cfg.dbname, charset = 'utf8')
        cur = conn.cursor()
        sql = 'SELECT `key`, `secret`, `adzoneid` FROM shz_appkey  WHERE ban_time < %d  order by RAND() limit 1' % int(time.time())
        try:
            cur.execute(sql)
            r = cur.fetchone()
            return r
        except Exception,e:
            print str(e)  + '???'
        finally:
            cur.close()
            conn.close()
            
    def updateBantime(self,key,bantime):
        conn = pymysql.connect (host = cfg.dbhost, port = cfg.dbport, user = cfg.dbuser, passwd = cfg.dbpass,db = cfg.dbname, charset = 'utf8')
        cur = conn.cursor ()
        sql = 'UPDATE shz_appkey SET ban_time = %d WHERE `key` = %s ' % (int(bantime) + int(time.time()) , key)
        try:
            cur.execute (sql)
            conn.commit()
        except Exception, e:
            print str(e) + '___up'
        finally:
            cur.close()
            conn.close()

    def make_steps(self,keyword,catid,start_price,end_price,step_size):
        try:
            for step in range(start_price,int(end_price)+1,step_size):
                start_step = step
                end_step = step + step_size
                for i in range(1,101):
                    resp = self.getItemList(i,start_step,end_step,keyword,catid)
                    itemsNum = resp['tbk_dg_material_optional_response']['total_results']
                    if itemsNum == 0:
                        break
                    else:
                        items = resp['tbk_dg_material_optional_response']['result_list']['map_data']
                        SaveItems ().checkExists (keyword,items,catid)
                        # 检查是否还有下一页
                        if len (items) < 100:
                            break
        except Exception , e:
            print str(e) + 'step'
            pass

