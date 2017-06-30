#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import re
import codecs
import hashlib
import urllib.parse
import urllib.request
import gzip
import json

cookies = 'DedeUserID=156117; SESSDATA=fe5e5d8e%2C1501398561%2C940e54b3;'

fake_headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Charset': 'UTF-8,*;q=0.5',
    'Accept-Encoding': 'gzip,deflate,sdch',
    'Accept-Language': 'en-US,en;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0',
    'cookie':cookies
}



def get_media_urls(cid):
    '''Request the URLs of the video

    Arguments: cid

    Return value: [media_urls]
    '''
    appkey = 'f3bb208b3d081dc8'
    SECRETKEY_MINILOADER = '1c15888dc316e05a15fdd0a02ed6584f'
    sign_this = hashlib.md5(bytes('cid={cid}&from=miniplay&player=1{SECRETKEY_MINILOADER}'.format(cid = cid, SECRETKEY_MINILOADER = SECRETKEY_MINILOADER), 'utf-8')).hexdigest()
    url = 'http://interface.bilibili.com/playurl?&cid=' + cid + '&from=miniplay&player=1' + '&sign=' + sign_this
    req = urllib.request.Request(url=url)
    response = urllib.request.urlopen(req, timeout=120)
    data = str(response.read())
    pattern=re.compile(r'.*?\[CDATA\[([^\]]*?\.mp4.*?)\]\].*?')
    matches=re.findall(pattern,data)
    urls=[]
    for match in matches:
        urls.append(match.replace('platform=pc','platform=iphone'))
    return urls


def getCid(aid):
    '''Request the cid of the video

    Arguments: aid

    Return value: cid in json 
    '''
    cid_url='http://www.bilibili.com/widget/getPageList?aid='+str(aid)
    req = urllib.request.Request(url=cid_url,headers=fake_headers)
    response = urllib.request.urlopen(req, timeout=120)
    content_encoding = response.getheader('Content-Encoding')
    if content_encoding == 'gzip':
        data = gzip.GzipFile(fileobj=response).read()
    elif content_encoding == 'deflate':
        decompressobj = zlib.decompressobj(-zlib.MAX_WBITS)
        data = decompressobj.decompress(response.read())+decompressobj.flush()
    else:
        data = response.read()
    data=json.loads(data.decode('utf-8', 'replace'))
    if len(data)<1:
        print('response error')
    else:
        return data

def getAid(url):
    '''Request the aid of the video

    Arguments: url of the video

    Return value: title,aid,img
    '''
    req=urllib.request.Request(url=url,headers=fake_headers)
    response=urllib.request.urlopen(req,timeout=120)
    content_encoding = response.getheader('Content-Encoding')
    if content_encoding == 'gzip':
        data = gzip.GzipFile(fileobj=response).read()
    elif content_encoding == 'deflate':
        decompressobj = zlib.decompressobj(-zlib.MAX_WBITS)
        data = decompressobj.decompress(response.read())+decompressobj.flush()
    else:
        data = response.read()
        
    aid=None
    title=None
    img=None
    regex = r"aid\s*=\s*[\'|\"](.+?)[\'|\"]"
    test_str = data.decode("utf8","ignore")
    matches = re.findall(regex, test_str, re.IGNORECASE | re.MULTILINE)
    if(matches):
        aid=matches[0]
    regex = r"wb_title\s*=\s*[\'|\"](.+?)[\'|\"]"
    matches = re.findall(regex, test_str, re.IGNORECASE | re.MULTILINE)
    if(matches):
        if "\\u" in matches[0]:
            title=matches[0].encode('utf8').decode('unicode_escape')
        else:
            title=matches[0]
    regex = r"wb_img\s*=\s*[\'|\"](.+?)[\'|\"]"
    matches = re.findall(regex, test_str, re.IGNORECASE | re.MULTILINE)
    if(matches):
        img=matches[0]
    return title,aid,img