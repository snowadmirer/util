#coding=utf-8

def download_from_url(url):
    res = urllib.requests.urlopen(url).read()
    return res
