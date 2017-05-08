#!/usr/bin/env python
# coding: utf-8
#

from wxbot import *
import urllib
import requests

class MYHWXBot(WXBot):

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
                                    

def main():
    bot = MYHWXBot()
    bot.DEBUG = True
    bot.conf['qr'] = 'tty'
    bot.run()


if __name__ == '__main__':
    main()
