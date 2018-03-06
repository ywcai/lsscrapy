# -*- coding: utf-8 -*-
"""
Created on Thu Feb 22 20:31:05 2018

@author: zmy_11
"""
import json  
import scrapy  
import random
import re
from lsscra.items import LsscraItem  
#import logging  
class myscrapySpider(scrapy.Spider):  
    name = "lsscrapy"  
    allowed_domains = ["www.c114.com.cn","www.csdn.net","blog.csdn.net"]  
    headers = {  
             'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'  
              }  

    start_urls = [  
#        "http://www.c114.com.cn/m2m/2493.html?page=1",#666
        "https://www.csdn.net/nav/news",
        "https://blog.csdn.net/nav/news",
        "https://www.csdn.net/nav/other",
        "https://www.csdn.net/nav/ai",
        "https://www.csdn.net/nav/blockchain",
        "https://www.csdn.net/nav/cloud",
#        "https://www.csdn.net/nav/cloud",#大数据 缺失
        "https://www.csdn.net/nav/iot",
        "https://www.csdn.net/nav/mobile",
        "https://www.csdn.net/nav/web",
        "https://www.csdn.net/nav/lang",
        "https://www.csdn.net/nav/db"
        ]
 
    def parse(self, response):  
        if response.status == 200:
           if self.allowed_domains[0] in response.url :
#              for payload in response.xpath("//div[@class='li3-2']//ul[@class='list1']/li"):
#                 item = LsscraItem()
#                 item['articletype']=6 #物联网分类
#                 item['quoteurl'],item['title'],item['createtime'] = payload.xpath(  
#                 "a/@href"  
#                 "|a/text()"  
#                 "|span/text()").extract()  
#                 detail_page_url = item['quoteurl']
#                 yield scrapy.Request(detail_page_url,callback=self.parse_c114_content,meta={'item': item})  
                 pass
           if self.allowed_domains[1] in response.url :
#             获取到的请求当前数据的边界然后请求真实的列表数据
              rex=r'.+nav/(.+)$'
              pattern = re.compile(rex) 
              m=pattern.match(response.url)
              titleType=m.group(1)
              offset=response.xpath("//ul[@shown-offset]//@shown-offset").extract()[0]
              base_csdn_url="http://blog.csdn.net/api/articles?type=more&category="+titleType+"&shown_offset="+offset
              yield scrapy.Request(base_csdn_url,callback=self.parse_csdn_index,meta={'mtype':titleType}) 
    #c114详细页面处理
    def parse_c114_content(self, response):  
        item=response.meta['item']
        if response.status == 200:
#            找文本长度长于5的第一段话作为摘要
            item['remarks']="这篇文章有点短，没有合适的摘要"
            for remarkPath in response.xpath("//div[@class='r3']//div[@class='text']/p"):
                if len(remarkPath.xpath('string(.)').extract()[0])>10:
                   item['remarks']=remarkPath.xpath('string(.)').extract()[0]
                   break
#                如果没有缩略图 ，赋值空
            thumbUrls=response.xpath("//div[@class='r3']//img[@witdh or @alt]/@src").extract()
            if thumbUrls:
               item['thumburl']=thumbUrls[0]
            else:
               item['thumburl']=""
            item['authnickname']="C114"
            item['authimg']=""    
            articlecontent=response.xpath("//div[@class='r3']//div[@class='text']").extract()[0]
#           过滤连接标签
            rex=r'<a.*?>|</a>'
            articlecontent=re.sub(rex,"",articlecontent)
#           过滤有width\height标签的       
            rex2=r'[wW]idth=.+?[\t ]'
            articlecontent=re.sub(rex2," width='98%' ",articlecontent)
            rex3=r'[Hh]eight=.+?[\t ]'
            articlecontent=re.sub(rex3," ",articlecontent)
#           过滤无width标签的  
#           先在response查找本来没有width标签
            noWidthImgs=response.xpath("//div[@class='r3']//img[not(@witdh) and @alt]").extract()
            for img in noWidthImgs:
                newImg=re.sub(r"<img","<img width='98%' ",img)
                articlecontent=articlecontent.replace(img,newImg)
                pass
            item['articlecontent']=articlecontent
            item['comment']=random.randint(100, 600)
            item['top']=random.randint(0, 80)
            item['pv']=random.randint(300, 2000)
            yield item
    def parse_csdn_index(self, response): 
        typeName=response.meta['mtype']
        temps = json.loads(response.body_as_unicode())  
        for temp in temps.get("articles"):
            temp["typeName"]=typeName
            yield scrapy.Request(temp.get("url"),callback=self.parse_csdn_content,meta={'temp': temp})
    def parse_csdn_content(self, response):
        temp=response.meta['temp']
    
        item = LsscraItem()
        if "news" in temp.get("typeName"):
             item["articletype"]=1
        if temp.get("typeName").lower()=="other".lower():
             item["articletype"]=1
        if temp.get("typeName").lower()=="ai".lower():
             item["articletype"]=2
        if temp.get("typeName").lower()=="blockchain".lower():
             item["articletype"]=3
        if temp.get("typeName")=="cloud":
             item["articletype"]=4
        if temp.get("typeName")=="bigdata":
             item["articletype"]=5
        if temp.get("typeName")=="iot":
             item["articletype"]=6
        if temp.get("typeName")=="mobile":
             item["articletype"]=7
        if temp.get("typeName")=="web":
             item["articletype"]=8
        if temp.get("typeName")=="lang":
             item["articletype"]=9
        if temp.get("typeName")=="db":
             item["articletype"]=10
        item['title']=temp.get("title")
        item['quoteurl']=temp.get("url")
        item['authnickname']=temp.get("nickname")
        item['authimg']="http:"+temp.get("avatar")
        item['pv']=temp.get("views")
        item['quoteurl']=temp.get("url")
        if response.status == 200:
            item['remarks']="文章没有合适的摘要信息"
            for remarkPath in response.xpath("//article//div[@class='htmledit_views']//p"):
                if len(remarkPath.xpath('string(.)').extract()[0])>30:
                    item['remarks']=remarkPath.xpath('string(.)').extract()[0]
                    break
#           如果没有缩略图 ，赋值空
            thumbUrls=response.xpath("//article//div[@class='htmledit_views']//img[@alt and @width and not(contains(@src,'gif'))]/@src").extract()
            item['thumburl']=""
            if thumbUrls:
               for thumburl in thumbUrls:
                   if "gif" in thumburl:
                       pass
                   else:
                       item['thumburl']=thumburl 
                       break             
            articlecontent=response.xpath("//article//div[@class='htmledit_views']").extract()[0]
            item['articlecontent']=articlecontent
            item['comment']=int(response.xpath("//dl[@title][4]/dd/text()").extract()[0])
            item['top']=int(response.xpath("//dl[@title][3]/dd/text()").extract()[0])
            yield item
            
  
    
        
