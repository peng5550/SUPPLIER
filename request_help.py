# -*- coding: utf-8 -*-
from urllib.parse import parse_qsl

def print_headers_raw_to_dict(headers_raw_l):
    print("{\n    '" + ",\n    ".join(map(lambda s: "'" +
        "': '".join(s.strip().split(': ')) + "'", headers_raw_l))[1:-1] + "'\n}")

def print_headers_raw_to_dict_space(headers_raw_l):
    print("{\n    '" + ",\n    ".join(map(lambda s: "'" + "': '".join(s.strip().split('\t')) + "'", headers_raw_l))[1:-1] + "'\n}")

def print_dict_from_copy_headers(headers_raw):
    headers_raw = headers_raw.strip()
    headers_raw_l = headers_raw.splitlines()

    if ':' in headers_raw_l[0]:
        print_headers_raw_to_dict(headers_raw_l)
    else:
        print_headers_raw_to_dict_space(headers_raw_l)

def print_url_params(url_params):
    s = str(parse_qsl(url_params.strip(), 1))
    print("OrderedDict(\n    " + "),\n    ".join(map(lambda s: s.strip(), s.split("),")))[1:-1] + ",\n)")

if __name__ == '__main__':
    header_text = '''
accept: application/json, text/plain, */*
accept-encoding: gzip, deflate, br
accept-language: zh-CN,zh;q=0.9
cookie: _bl_uid=j8k9hgetujLlIz8I69RUo4artheq; t=8hODXjQUMhnEm0jh; wt=8hODXjQUMhnEm0jh; JSESSIONID=""; Hm_lvt_194df3105ad7148dcf2b98a91b5e727a=1603963325,1604017808; Hm_lpvt_194df3105ad7148dcf2b98a91b5e727a=1604017808; __g=-; __c=1604017808; __l=l=%2Fwww.zhipin.com%2Fweb%2Fboss%2Fsearch&r=&g=&friend_source=0&friend_source=0; __a=23774869.1603963323.1603963323.1604017808.6.2.3.6
referer: https://www.zhipin.com/vue/index/
sec-fetch-dest: empty
sec-fetch-mode: cors
sec-fetch-site: same-origin
token: YhwjhEWC1tw6kmM
user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36
x-anti-request-token: d41d8cd98f00b204e9800998ecf8427e
x-requested-with: XMLHttpRequest

'''

    print_dict_from_copy_headers(header_text)



