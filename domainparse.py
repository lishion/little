import re
from urllib.parse import urlparse
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
 
def parse(url):
    url_trimed = url.strip(" ")
    if not ( url_trimed.startswith("http://") or url_trimed.startswith("https://") ):
        url_trimed = "http://" + url_trimed
    host = urlparse(url_trimed).netloc
    m = pattern.search(host)
    res =  m.group() if m else host
    return res if res else url
  
if __name__ == "__main__":
    print ( parse("www.test.com") )
    print ( parse("app.test.cn") )
    print ( parse("http://www.test.edu.cn") )
    print ( parse("www.test.gov.cn?sfsaerfsdsfwefasdfsdfs/sfsd.dsfsfd") )