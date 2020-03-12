#coding=utf-8
import re
import requests
import shutil
import os
from urllib.parse import quote
import string
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
def get_url_content(url):
    url = quote(url, safe=string.printable)
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

def get_driver(web_tool):

    option = webdriver.ChromeOptions()
    #option.add_argument('headless')
    option.add_argument('disable-infobars')
    option.add_experimental_option('excludeSwitches', ['enable-logging'])
    prefs = {
        'profile.default_content_setting_values' : {
            'images' : 2
        }
    }
    #option.add_experimental_option('prefs',prefs)
    driver = webdriver.Chrome(web_tool, options=option)
    return driver

def right_click_save(webdriver, xpath):
    wait = WebDriverWait(driver,10)
    img = wait.until(EC.element_to_be_clickable((By.TAG_NAME,'img')))
    actions = ActionChains(driver)
    actions.context_click(img)
    actions.perform()

    pyautogui.typewrite(['down', 'down'])
    sleep(1)
    pyautogui.typewrite(['enter', 'enter'])
    sleep(1)
    pyautogui.typewrite(['enter', 'enter'])
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
