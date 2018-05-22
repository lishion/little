from dns.resolver import query
import requests
import re
from bs4 import BeautifulSoup
from auto_decode import decode


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
