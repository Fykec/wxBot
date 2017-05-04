#!/usr/bin/env python
# coding: utf-8
#

from wxbot import *
import datetime
import urllib
import requests
from pyquery import PyQuery as pq

from apscheduler.schedulers.background import BackgroundScheduler


NEWS_SOURCE_URL = ""
SHORTEN_URL = ""
TEST_USER = u""
SCHEDULE_HOUR = 8
SCHEDULE_MINUTE = 0

class NewsWXBot(WXBot):

    def handle_msg_all(self, msg):
        #群昵称，进群之后，必须改为这个昵称
        self.nickName = u'小猫助手'
        reload(sys) 
        sys.setdefaultencoding('utf8')
        ##群文本消息
        if msg['msg_type_id'] == 3 and msg['content']['type'] == 0:
            #群名是unknown，重新获取一遍联系人
            if msg['user']['name'] == 'unknown' or msg['content']['user']['name'] == 'unknown':
                print 'get contact again'
                self.get_contact()
            #@了
            if msg['content']['data'].find('@'+self.nickName) != -1:
                if msg['content']['data'].find(u'论坛') != -1:
                    self.send_msg_by_uid(u'@'+msg['content']['user']['name']+' http://t.cn/RiZuWNK', msg['user']['id'])

        if msg['msg_type_id'] == 4 and msg['content']['type'] == 0:
            self.send_msg_by_uid(u'hi', msg['user']['id'])

    def getShortUrl(self, longUrl):    
        shortenURL = SHORTEN_URL + urllib.quote_plus(longUrl)        
        res = requests.get(shortenURL)
        json = res.json()
        if len(json) and json[0]["url_short"]:
            return json[0]["url_short"]

        return longUrl

    def getNews(self):  
        print("Get News Started")
        dateText = datetime.datetime.now().strftime("%Y-%m-%d") # like: '2017-04-28'      
        doc = pq(url=NEWS_SOURCE_URL)      
        contentList = doc(".table-content tbody tr")
        news = "Test content"
        itemIssueText = ""
        for item in contentList:
            itemContent = pq(item)
            itemDateText = itemContent("td:first").text()
            
            if dateText in itemDateText:
                itemIssueText = itemContent("td:nth-child(2)").text()
                divTextArray = itemContent("td div").text().split(" ")  
                newsList = []              
                newsItem = {}
                tempTitle = None
                tempUrl = None                
                for divText in divTextArray[2:]: #  '2:' is from the first news's td element
                    if tempTitle is None:
                        tempTitle = divText
                    elif tempUrl is None:
                        tempUrl = self.getShortUrl(divText)
                        newsList.append({"title": tempTitle, "url": tempUrl})
                        tempTitle = None
                        tempUrl = None

                # print(newsList)   
        
        newsTitle = u"猫友早报：【第" + itemIssueText + u"期】"  
        news = newsTitle + "\n\n"
        for newsItem in newsList:
            news = news + newsItem["title"] + "\n" + newsItem["url"] + "\n\n"        
        self.send_msg(TEST_USER, news)
    
    def scheduleNews(self):
        scheduler = BackgroundScheduler()
        scheduler.add_job(self.getNews, 'cron', hour=SCHEDULE_HOUR, minute=SCHEDULE_MINUTE)        
        scheduler.start()                            
        print("Schedule News Started")
                                    

def main():
    bot = NewsWXBot()
    bot.DEBUG = True
    bot.conf['qr'] = 'png'
    bot.scheduleNews()
    bot.run()


if __name__ == '__main__':
    main()
