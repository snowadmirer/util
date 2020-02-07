#coding=utf-8
import re
import requests
import shutil
import os
from time import sleep

def get_url_content(url):
    res = urllib.request.urlopen(url).read()
    return res

def write_content(content, filepath):
    with open(filepath, 'wb') as f:
        f.write(content)

def get_img_name_from_url(url):
    res = re.findall('[-\w]+.[j]?p[ne]?g', url)
    if res:
        return res[0]
    return None
 
def download_baidu_pic(html,keyword, save_dir, index):
 
    pic_url = re.findall('"objURL":"(.*?)",',html,re.S)
    print ('找到关键词:'+keyword+'的图片，现在开始下载图片...')
    for each in pic_url:
        print ('正在下载第'+str(index+1)+'张图片，图片地址:'+str(each))
        try:
            pic= requests.get(each, timeout=10, allow_redirects=False)
        except Exception as e:
            print ('【错误】当前图片无法下载')
            continue
 
        string = os.path.join(save_dir, '{:04d}.jpg'.format(index))
        #resolve the problem of encode, make sure that chinese name could be store
        fp = open(string,'wb')
        fp.write(pic.content)
        fp.close()
        index += 1
    return index

def clean_dir(save_dir):
    if os.path.exists(save_dir):
        shutil.rmtree(save_dir)
    os.mkdir(save_dir)

if __name__ == '__main__':
    word = input("Input key word: ")
    save_dir = word
    clean_dir(save_dir)
    index = 0
    for pag_id in range(30):
        pn = 20 * pag_id
        url = 'http://image.baidu.com/search/flip?tn=baiduimage&ie=utf-8&word={}&pn={}&gsm=&ct=&ic=0&lm=-1&width=0&height=0'.format(word, pn)
        result = requests.get(url)
        index = download_baidu_pic(result.text,word, save_dir, index)
        sleep(1)
