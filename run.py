#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on May 29, 2020
Desc: Twitter feed to toot (based on RSSHub's feed)
Author: Mashiro 
URL: https://2heng.xin
License: MIT
"""
from utils.feed_parser import FeedParaser
from utils.feed2toot import Feed2Toot
from utils.get_config import GetConfig
import os

config = GetConfig()
user_id = 0
user_count = int(str(config.sections()).count('USER'))-1

if __name__ == '__main__':
  if config['PROXY']['ProxyOn'] == 'true':
    os.environ['HTTP_PROXY'] = config['PROXY']['HttpProxy']
    os.environ['HTTPS_PROXY'] = config['PROXY']['HttpsProxy']
    
  while user_id <= user_count:
    user_name = 'USER'+str(user_id)
    RSS_dict = FeedParaser(config[user_name]['Rss'])
    Feed2Toot(user_name, RSS_dict)
    user_id += 1
  
