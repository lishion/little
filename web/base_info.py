from dns.resolver import query
import requests
import re
from bs4 import BeautifulSoup
from auto_decode import decode
from urllib.parse import urlparse

def simple_dns(url):
    """
    Args:域名，不能包含http(s)://
    """

    data = query(url)
    ips = [x.to_text() for x in data.response.answer]
    pattern = r"\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b"
    return re.findall(pattern, "".join(ips))

def get_title(url):
    """
    爬取网站标题，可避免中文乱码，依赖于decode模块
    https://github.com/lishion/little/blob/master/auto_decode.py
    """
    try:
        headers = {"accept": "text/html,application/xhtml+xml,application/xml;",
                   "accept-encoding": "gzip",
                   "x-forwarded-for": "123.125.66.120",
                   "accept-language": "zh-cn,zh;q=0.8",
                   "referer": "https://www.baidu.com",
                   "connection": "keep-alive",
                   "user-agent": "Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)"
                   }
        html = requests.get(url, headers=headers,timeout=3)
        if html.status_code != 200:
            return {"title":"","other":"无法访问,code: " + str(html.status_code)}
        text,encoding = decode(html)
        tree = BeautifulSoup(text,"lxml")
        if tree.title:
            return {"title":tree.title.text,"other":"爬取成功"}
        else:
            return {"title":"","other":"网页中不存在title"}
    except BaseException as e:
        return {"title":"","other":"连接到服务器失败: " + str(e)}

def domain(url):
    """
        从url中获取域名:
        https://www.test.com?q=12313 -> www.test.com
    """
    parse_url = url
    if "://" not in url:
        parse_url = "http://" + url
    return urlparse(parse_url).netloc

topHostPostfix = (
    '.com','cn','la','.io','.co','.info','.net','.org','.me','.mobi',
    '.us','.biz','.xxx','.ca','.co.jp','.com.cn','.net.cn',
    '.org.cn','.mx','.tv','.ws','.ag','.com.ag','.net.ag',
    '.org.ag','.am','.asia','.at','.be','.com.br','.net.br',
    '.bz','.com.bz','.net.bz','.cc','.com.co','.net.co',
    '.nom.co','.de','.es','.com.es','.nom.es','.org.es',
    '.eu','.fm','.fr','.gs','.in','.co.in','.firm.in','.gen.in',
    '.ind.in','.net.in','.org.in','.it','.jobs','.jp','.ms',
    '.com.mx','.nl','.nu','.co.nz','.net.nz','.org.nz',
    '.se','.tc','.tk','.tw','.com.tw','.idv.tw','.org.tw',
    '.hk','.co.uk','.me.uk','.org.uk','.vg', ".com.hk",".cn",".edu",'.info','.app',
    '.edu.cn','.gov.cn'
    
    )
regx = r'[^\.]+('+'|'.join([h.replace('.',r'\.') for h in topHostPostfix])+')$'
pattern = re.compile(regx,re.IGNORECASE)

def basedomian(url):
    """
        从url、域名中获取主域名
        (https://)www.test.com -> test.com
    """
    url_trimed = url.strip(" ")
    if not ( url_trimed.startswith("http://") or url_trimed.startswith("https://") ):
        url_trimed = "http://" + url_trimed
    host = urlparse(url_trimed).netloc
    m = pattern.search(host)
    res =  m.group() if m else host
    return res if res else url