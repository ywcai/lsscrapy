# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
#import json

import time
import pymysql
from scrapy.conf import settings 
class LsscraPipeline(object):
    def __init__(self):  
          host = settings['MYSQL_HOSTS']  
          user = settings['MYSQL_USER']  
          psd =  settings['MYSQL_PASSWORD']  
          db = settings['MYSQL_DB']  
          c=  settings['CHARSET']
          port=  settings['MYSQL_PORT'] 
          self.con=pymysql.connect(host=host,user=user,passwd=psd,db=db,charset=c,port=port)  
    def close_spider(self, spider):
          self.con.close()  

    def process_item(self, item, spider):
        cue=self.con.cursor()   
        checkIsExistSql="select id from article where quoteurl = %s "
        selectData=(self.con.escape(item['quoteurl']))
        try:
            rows=cue._query(checkIsExistSql%selectData)
        except Exception as e:  
            print('Insert error:',e)  
            self.con.rollback()
            return [""]
        else:  
            self.con.commit()
        if rows>0:
#            print('------------------------------------数据已经存在-------------------------------------')  
            return ""
        sql="insert into article (articletype,authimg,authnickname,comment,createtime,pv,remarks,thumburl,title,top,articlecontent,quoteurl) "\
        "values(%d,%s,%s,%d,%s,%d,%s,%s,%s,%d,%s,%s)"
        nowTime=time.strftime("%Y-%m-%d %H:%M")
        insertdata=(
             item['articletype'],
             self.con.escape(item['authimg']),
             self.con.escape(item['authnickname']),
             item['comment'],
             self.con.escape(nowTime),
             item['pv'],
             self.con.escape(item['remarks']),
             self.con.escape(item['thumburl']),
             self.con.escape(item['title']),
             item['top'],
             self.con.escape(item['articlecontent']),
             self.con.escape(item['quoteurl']))
#        #数据库游标
        try:  
            cue.execute(sql%insertdata)
#            print("insert success")#测试语句  
        except Exception as e:  
            print('Insert error:',e)  
            self.con.rollback()  
        else:  
            self.con.commit()  
        return ""
    