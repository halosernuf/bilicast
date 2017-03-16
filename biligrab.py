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
import logging


USER_AGENT_PLAYER = 'Mozilla/5.0 BiliDroid/4.24.0 (bbcallen@gmail.com)'
# USER_AGENT_API = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.116 Safari/537.36'
USER_AGENT_API="Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.76 Mobile Safari/537.36"
APPKEY = '1q8o6' + 'r7q4523' + '3436'   # Unknown source
APPSEC = '560p52ppq288' + 'srq045859rq18' + 'ossq973'    # Do not abuse please, get one yourself if you need
# APPKEY = 'f3bb208b3d081dc8'
# APPSEC = '1c15888dc316e05a15fdd0a02ed6584f' 

BILIGRAB_HEADER = {'User-Agent': USER_AGENT_API, 'Cache-Control': 'no-cache', 'Pragma': 'no-cache'}

url_get_metadata= 'http://api.bilibili.com/view?'
url_get_media = 'http://interface.bilibili.com/playurl?'
# cookie='{ "domain": ".bilibili.com", "expirationDate": 1514072483, "hostOnly": false, "httpOnly": false, "name": "_cnt_dyn", "path": "/", "sameSite": "no_restriction", "secure": false, "session": false, "storeId": "0", "value": "null", "id": 1 }, { "domain": ".bilibili.com", "expirationDate": 1514072483, "hostOnly": false, "httpOnly": false, "name": "_cnt_notify", "path": "/", "sameSite": "no_restriction", "secure": false, "session": false, "storeId": "0", "value": "17", "id": 2 }, { "domain": ".bilibili.com", "expirationDate": 1514072483, "hostOnly": false, "httpOnly": false, "name": "_cnt_pm", "path": "/", "sameSite": "no_restriction", "secure": false, "session": false, "storeId": "0", "value": "0", "id": 3 }, { "domain": ".bilibili.com", "expirationDate": 1482540075.497237, "hostOnly": false, "httpOnly": true, "name": "_dfcaptcha", "path": "/", "sameSite": "no_restriction", "secure": false, "session": false, "storeId": "0", "value": "4934c39506901e08d76e0ae70222cf72", "id": 4 }, { "domain": ".bilibili.com", "expirationDate": 1484249844.151035, "hostOnly": false, "httpOnly": false, "name": "_ver", "path": "/", "sameSite": "no_restriction", "secure": false, "session": false, "storeId": "0", "value": "1", "id": 5 }, { "domain": ".bilibili.com", "expirationDate": 1576463307.959116, "hostOnly": false, "httpOnly": false, "name": "buvid3", "path": "/", "sameSite": "no_restriction", "secure": false, "session": false, "storeId": "0", "value": "5E523CC1-7426-422B-9C89-BB4946D238F519745infoc", "id": 6 }, { "domain": ".bilibili.com", "expirationDate": 1484249844.150405, "hostOnly": false, "httpOnly": false, "name": "ck_pv", "path": "/", "sameSite": "no_restriction", "secure": false, "session": false, "storeId": "0", "value": "S9M9IJ", "id": 7 }, { "domain": ".bilibili.com", "expirationDate": 1487908477.546286, "hostOnly": false, "httpOnly": false, "name": "DedeID", "path": "/", "sameSite": "no_restriction", "secure": false, "session": false, "storeId": "0", "value": "5262155", "id": 8 }, { "domain": ".bilibili.com", "expirationDate": 1484249844.14941, "hostOnly": false, "httpOnly": false, "name": "DedeUserID", "path": "/", "sameSite": "no_restriction", "secure": false, "session": false, "storeId": "0", "value": "156117", "id": 9 }, { "domain": ".bilibili.com", "expirationDate": 1484249844.149846, "hostOnly": false, "httpOnly": false, "name": "DedeUserID__ckMd5", "path": "/", "sameSite": "no_restriction", "secure": false, "session": false, "storeId": "0", "value": "d45001b561b8124c", "id": 10 }, { "domain": ".bilibili.com", "expirationDate": 1540027593, "hostOnly": false, "httpOnly": false, "name": "fts", "path": "/", "sameSite": "no_restriction", "secure": false, "session": false, "storeId": "0", "value": "1445433993", "id": 11 }, { "domain": ".bilibili.com", "expirationDate": 1540600078.867845, "hostOnly": false, "httpOnly": false, "name": "LIVE_BUVID", "path": "/", "sameSite": "no_restriction", "secure": false, "session": false, "storeId": "0", "value": "350fc3717b817b477073fad36c0480cf", "id": 12 }, { "domain": ".bilibili.com", "expirationDate": 1540600078.867929, "hostOnly": false, "httpOnly": false, "name": "LIVE_BUVID__ckMd5", "path": "/", "sameSite": "no_restriction", "secure": false, "session": false, "storeId": "0", "value": "9519593b46778c0a", "id": 13 }, { "domain": ".bilibili.com", "expirationDate": 2147385600, "hostOnly": false, "httpOnly": false, "name": "pgv_pvi", "path": "/", "sameSite": "no_restriction", "secure": false, "session": false, "storeId": "0", "value": "7708942336", "id": 14 }, { "domain": ".bilibili.com", "hostOnly": false, "httpOnly": false, "name": "pgv_si", "path": "/", "sameSite": "no_restriction", "secure": false, "session": true, "storeId": "0", "value": "s930134016", "id": 15 }, { "domain": ".bilibili.com", "expirationDate": 1668121200.292351, "hostOnly": false, "httpOnly": false, "name": "rpdid", "path": "/", "sameSite": "no_restriction", "secure": false, "session": false, "storeId": "0", "value": "ooiipxlwpsdopqoomqoiw", "id": 16 }, { "domain": ".bilibili.com", "expirationDate": 1484249844.149958, "hostOnly": false, "httpOnly": true, "name": "SESSDATA", "path": "/", "sameSite": "no_restriction", "secure": false, "session": false, "storeId": "0", "value": "fe5e5d8e%2C1484249844%2Cdfee2f3b", "id": 17 }, { "domain": ".bilibili.com", "expirationDate": 1512975078.321604, "hostOnly": false, "httpOnly": false, "name": "sid", "path": "/", "sameSite": "no_restriction", "secure": false, "session": false, "storeId": "0", "value": "89fil159", "id": 18 }, { "domain": ".bilibili.com", "expirationDate": 1484249844.150704, "hostOnly": false, "httpOnly": false, "name": "SSID", "path": "/", "sameSite": "no_restriction", "secure": false, "session": false, "storeId": "0", "value": "5nQ0CcuIRUUgvOLeHnH3Qzubvb7NO13ck3o36A5GsqanDwl_a2qkfB9LXXSviaGjYYv49_a_b2HMHkNQZmEU1cIxZIBqzquYhbHQGGubaaeZgI_c", "id": 19 }, { "domain": ".bilibili.com", "expirationDate": 2398377600, "hostOnly": false, "httpOnly": false, "name": "uTZ", "path": "/", "sameSite": "no_restriction", "secure": false, "session": false, "storeId": "0", "value": "300", "id": 20 }, { "domain": "www.bilibili.com", "expirationDate": 1498261283, "hostOnly": true, "httpOnly": false, "name": "CNZZDATA2724999", "path": "/", "sameSite": "no_restriction", "secure": false, "session": false, "storeId": "0", "value": "cnzz_eid%3D91166475-1445433992-%26ntime%3D1482531525", "id": 21 }'
cookie=None
source=None
quality=3
fakeip=None

def fetch_url(url, *, user_agent=USER_AGENT_PLAYER, cookie=None, fakeip=None):
    '''Fetch HTTP URL

    Arguments: url, user_agent, cookie

    Return value: (response_object, response_data) -> (http.client.HTTPResponse, bytes)
    '''
    logging.debug('Fetch: %s' % url)
    req_headers = {'User-Agent': user_agent, 'Accept-Encoding': 'gzip, deflate'}
    if cookie:
        req_headers['Cookie'] = cookie
    if fakeip:
        req_headers['X-Forwarded-For'] = fakeip
        req_headers['Client-IP'] = fakeip
        # req_headers['X-Real-IP'] = fakeip
    req = urllib.request.Request(url=url, headers=req_headers)
    response = urllib.request.urlopen(req, timeout=120)
    content_encoding = response.getheader('Content-Encoding')
    if content_encoding == 'gzip':
        data = gzip.GzipFile(fileobj=response).read()
    elif content_encoding == 'deflate':
        decompressobj = zlib.decompressobj(-zlib.MAX_WBITS)
        data = decompressobj.decompress(response.read())+decompressobj.flush()
    else:
        data = response.read()
    return response, data

def get_media_urls(cid, fuck_you_bishi_mode=False):
    '''Request the URLs of the video

    Arguments: cid

    Return value: [media_urls]
    '''
    if source in {None, 'overseas'}:
        user_agent = USER_AGENT_API if not fuck_you_bishi_mode else USER_AGENT_PLAYER
        req_args = {'cid': cid}
        if quality is not None:
            req_args['quality'] = quality
        else:
            req_args['quality'] = None
        _, response = fetch_url(url_get_media+andro_mock(req_args), user_agent=user_agent, cookie=cookie, fakeip=fakeip)
        '''
        media_urls = [str(k.wholeText).strip() for i in xml.dom.minidom.parseString(response.decode('utf-8', 'replace')).getElementsByTagName('durl') for j in i.getElementsByTagName('url')[:1] for k in j.childNodes if k.nodeType == 4]
        '''
        json_obj = json.loads(response.decode('utf-8'))
        if json_obj['result'] != 'suee':  # => Not Success
            raise ValueError('Server returned an error: %s (%s)' % (json_obj['result'], json_obj['code']))
        media_urls = [str(i['url']).strip() for i in json_obj['durl']]
        if not fuck_you_bishi_mode and media_urls == ['http://static.hdslb.com/error.mp4']:
            logging.error('Detected User-Agent block. Switching to fuck-you-bishi mode.')
            return get_media_urls(cid, fuck_you_bishi_mode=True)
    elif source == 'html5':
        req_args = {'aid': aid, 'page': pid}
        logging.warning('HTML5 video source is experimental and may not always work.')
        print('http://www.bilibili.com/m/html5?'+urllib.parse.urlencode(req_args))
        _, response = fetch_url('http://www.bilibili.com/m/html5?'+urllib.parse.urlencode(req_args), user_agent=USER_AGENT_PLAYER)
        response = json.loads(response.decode('utf-8', 'replace'))
        media_urls = [dict.get(response, 'src')]
        if not media_urls[0]:
            media_urls = []
        if not fuck_you_bishi_mode and media_urls == ['http://static.hdslb.com/error.mp4']:
            logging.error('Failed to request HTML5 video source. Retrying.')
            return get_media_urls(cid, fuck_you_bishi_mode=True)
    elif source == 'flvcd':
        req_args = {'kw': url}
        if quality is not None:
            if quality == 3:
                req_args['quality'] = 'high'
            elif quality >= 4:
                req_args['quality'] = 'super'
        _, response = fetch_url('http://www.flvcd.com/parse.php?'+urllib.parse.urlencode(req_args), user_agent=USER_AGENT_PLAYER)
        resp_match = re.search('<input type="hidden" name="inf" value="([^"]+)"', response.decode('gbk', 'replace'))
        if resp_match:
            media_urls = resp_match.group(1).rstrip('|').split('|')
        else:
            media_urls = []
    elif source == 'bilipr':
        req_args = {'cid': cid}
        quality_arg = '1080' if quality is not None and quality >= 4 else '720'
        logging.warning('BilibiliPr video source is experimental and may not always work.')
        resp_obj, response = fetch_url('http://pr.lolly.cc/P%s?%s' % (quality_arg, urllib.parse.urlencode(req_args)), user_agent=USER_AGENT_PLAYER)
        if resp_obj.getheader('Content-Type', '').startswith('text/xml'):
            media_urls = [str(k.wholeText).strip() for i in xml.dom.minidom.parseString(response.decode('utf-8', 'replace')).getElementsByTagName('durl') for j in i.getElementsByTagName('url')[:1] for k in j.childNodes if k.nodeType == 4]
        else:
            media_urls = []
    else:
        assert source in {None, 'overseas', 'html5', 'flvcd', 'bilipr'}
    if len(media_urls) == 0 or media_urls == ['http://static.hdslb.com/error.mp4']:
        raise ValueError('Can not get valid media URLs.')
    return media_urls


def bilibili_hash(args):
    '''Calculate API signature hash

    Arguments: {request_paramter: value}

    Return value: hash_value -> str
    '''
    return hashlib.md5((urllib.parse.urlencode(sorted(args.items()))+codecs.decode(APPSEC,'rot13')).encode('utf-8')).hexdigest()  # Fuck you bishi

    
def andro_mock(params):
    '''Simulate Android client

    Arguments: params

    Return value: request_string -> str
    '''
    import random
    import base64
    import collections
    our_lvl = 412
    _, api_response = fetch_url('http://app.bilibili.com/mdata/android3/android3.ver', user_agent=USER_AGENT_API)
    api_lvl = int(json.loads(api_response.decode('utf-8'))['upgrade']['ver'])
    logging.debug('Our simulated API level: %s, latest API level: %s' % (our_lvl, api_lvl))
    if api_lvl > our_lvl:
        logging.warning('Bilibili API server indicates the API protocol has been updated, the extraction may not work!')
    # fake_hw = random.Random().randrange(start=0, stop=18000000000000000084).to_bytes(8, 'big').hex()
    fake_hw = codecs.encode(random.Random().randrange(start=0, stop=18000000000000000084).to_bytes(8, 'big'),'hex_codec')
    add_req_args = collections.OrderedDict({
        'platform' : 'android',
        '_device': 'android',
        # '_appver': '424000',
        '_buvid':'A4ADF689-119D-425B-B158-E123DC73660646732infoc',
        '_appver': '429100',
        '_p': '1',
        '_down': '0',
        'cid': params['cid'],
        '_tid': '0',
        'otype': 'json',
        'type':'mp4',
        '_hwid': fake_hw
        })
    if params['quality'] is not None:
                add_req_args['quality'] = params['quality']
    # second_key = 'G&M40GdVRlW-v53V=yvd'
    # second_sec = 'W;bIwGB##4G&y29Vr64yF=H|}HZ(LjH8?gmHeoU`'
    second_key= b'452d3958f048c02a'
    second_sec= 'f7c926f549b9becf1c27644958676a21'
    add_req_args['appkey'] = second_key
    req_args = add_req_args
    add_req_args= collections.OrderedDict(sorted(req_args.items()))
    req_args['sign'] = hashlib.md5(bytes(urllib.parse.urlencode(add_req_args) + second_sec, 'utf-8')).hexdigest()
    return urllib.parse.urlencode(req_args)

def getCid(aid):
    # aid=3834172
    cid_url='http://www.bilibili.com/widget/getPageList?aid='+str(aid)
    req = urllib.request.Request(url=cid_url)
    response = urllib.request.urlopen(req, timeout=120)
    content_encoding = response.getheader('Content-Encoding')
    if content_encoding == 'gzip':
        data = gzip.GzipFile(fileobj=response).read()
    elif content_encoding == 'deflate':
        decompressobj = zlib.decompressobj(-zlib.MAX_WBITS)
        data = decompressobj.decompress(response.read())+decompressobj.flush()
    else:
        data = response.read()
    # r=response.read().decode('utf-8')
    # print(data.decode('utf-8', 'replace'))
    data=json.loads(data.decode('utf-8', 'replace'))
    if len(data)<1:
        print('response error')
    else:
        # for page in data:
            # print(page['page'])
            # print(page['pagename'])
            # print(page['cid'])
            # media_urls = get_media_urls(page['cid'])
            # page['url']=media_urls[0]
        return data

def getAid(url):
    req=urllib.request.Request(url=url)
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

# print(get_media_urls(12502101))