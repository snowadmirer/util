#coding=utf-8
import re
import requests
import time
import random
from pprint import pprint
from tqdm import tqdm

def get_douban_topics(group_name, max_page):
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 \
           (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36'}
    topics = []
    group_url = "https://www.douban.com/group/%s/"%(group_name)
    group_text = requests.get(group_url, headers=headers).text.replace("\n", "")
    if not group_text:
        return topics
    try:
        title = re.search("<title>(.*?)</title>", group_text).group(1).strip()
    except:
        print(group_text)
        return []
    print(title)
    for i in tqdm(range(max_page)):
        url = "https://www.douban.com/group/%s/discussion?start=%d"%(group_name, i*25)
        text = requests.get(url, headers=headers).text.replace("\n", "")
        if not text:
            break
        for topic_tr in re.findall('<tr class="">.*?</tr>', text):
            title_td = re.search('<td class="title">.*?</td>', topic_tr).group(0)
            topic_url = re.search('a href="(.*?)"', title_td).group(1)
            title = re.search('title="(.*?)" class="">', title_td).group(1)
            content = re.search('" class="">(.*?)</a>', title_td).group(1).strip()
            author_td = re.search('<td nowrap="nowrap">.*?</td>', topic_tr).group(0)
            author_url = re.search('a href="(.*?)"', author_td).group(1)
            author_name = re.search('class="">(.*?)</a>', author_td).group(1)
            topics.append((topic_url, title, content, author_url, author_name))
            time.sleep(random.uniform(1.0, 3.0))
    return topics
