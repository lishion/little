from dns.resolver import query
import requests
import re
from bs4 import BeautifulSoup

def simple_dns(url):
    data = query(url)
    ips = [x.to_text() for x in data.response.answer]
    pattern = r"\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b"
    return re.findall(pattern, "".join(ips))

def get_title(url):
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
            return {"title":"","other":"无法访问, code: " + str(html.status_code)}
        coding = requests.utils.get_encodings_from_content(html.text)
        tree = BeautifulSoup(html.content.decode(coding[0] if coding else "utf-8"),"lxml")

        if tree.title:
            return {"title":tree.title.text,"other":""}
        else:
            return {"title":"","other":"爬取title失败"}
    except BaseException as e:
        return {"title":"","other":str(e)}