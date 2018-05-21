import requests

debug = False

def get_encoding(response):
    encoding_from_meta = requests.utils.get_encodings_from_content(response.text)
    if encoding_from_meta:
        return encoding_from_meta[0]
    else:
        return response.apparent_encoding

def use_all_encoding(response):
    encodings = ['utf-8','gb2312','gbk']
    for encoding in encodings:
        try:
            text =  response.content.decode(encoding)
            debug and print(f'[*] using encoding {encoding} success')
            return text,encoding
        except:
            debug and print(f'[x] using encoding {encoding} error')
            pass
    return response.text,'not find'

def decode(response):

    if response.encoding == 'ISO-8859-1':
       
        try:
            encoding = get_encoding(response)
            debug and print(f'[*] no charset in http header find ')
            text =  response.content.decode(encoding)
            debug and print(f'[*] using encoding {encoding} success')
            return text,encoding
        except:
            debug and print(f'[x] using encoding {encoding} error')
            pass
    else:

        debug and print(f'[*] {response.encoding} find in http header ')
        return response.text,response.encoding

    return use_all_encoding(response)
