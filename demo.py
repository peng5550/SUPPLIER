import requests
import json
from lxml import etree
import re

# session = requests.Session()
#
# headers = {
#     # ':authority': 'connect.asicentral.com',
#     # ':method': 'GET',
#     # ':path': '/CreditReport/CRProfile?ID=119732&Source=MonitorDetail',
#     # ':scheme': 'https',
#     'accept': 'text/html, */*; q=0.01',
#     'accept-encoding': 'gzip, deflate, br',
#     'accept-language': 'zh-CN,zh;q=0.9',
#     'cookie': 'RefreshCookie=107b3867-f5d7-4ee9-a471-2a9e315b788d; AuthCookie=eyJhbGciOiJSU0EtT0FFUCIsImVuYyI6IkEyNTZHQ00iLCJrZXlpZCI6IkNPTk4ifQ.Y0SnsJOyCpEd-cCvXcn2A4i9JLIVe2mJrzNFzFEFAW8D5D599El1pAlEq5N7ixai4A6w5GCB1aMIi1lccyOwamHlE87FC0E_GJurOgTw136zJxB_USli5DAQ-De3OreR_NMspOGfZN-1wOBm098e9gzhQs4lnHxV3PmetiEeJTM.MXMaesUbTVsGPn8s.L-YEMIr-tYjAJpVRd2FKu_izXlEaJr6dOF3N4dK1GO-uaiiH0LGg6T802j5HQXyQGZHrZDJb48iEpaibkiabXP4DV8J04ZeaYI9JdyCwPvqX8lXr3JxP2f8l4p4eY7qzGcC9u-f0PhvcW92yyty486LS8ub_qaYNShMB8aYH4vGsiBc00DdtVlCDbrYeg8IUiMxjaX0eZDKTWRlMD3xGmaK8rggEpJiocUcOerb9Q5FWegCtHDcgwNWoa9fYP2cqr8ODnIG5is_3k_CU8FnOH0odb2B1GfX4Z19qKzV7Wi8sRXZnPw3a_gse-gfK9EE8bAilzKA9K9Pib-weDV46SD-3aPtp-K4HcMwj-zmmT68XXcmsLGdnmtYp895_RCs5qTe6iY0sfPlsdS7MWMbqYkiWLLT7gmP8LX5HB_4_ZcVdWfyKt30ar5GrANUJ-86X24FIhOcJ3w9jGoBhhy-tfNlZqZBQ6yy28Z5ngzqva_wOkW36RGOBhd-u5lyGrj04dGw-Vk1DTbQ7-WPnBQ0dmiKOmf5pXvQEfKyE.ueJ7uqxK2eFfIjKEDoTubQ',
#     # 'referer': 'https://connect.asicentral.com/MonitorDetailReport/Index/119732',
#     # 'sec-fetch-dest': 'empty',
#     # 'sec-fetch-mode': 'cors',
#     # 'sec-fetch-site': 'same-origin',
#     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36',
#     'x-requested-with': 'XMLHttpRequest'
# }
#
# session.headers = headers

# login_url = "https://connect.asicentral.com/Login//Home/LoginUser"
# login_data = {"AsiNumber": "59711", "UserName": "rommel@harrycreativepromos.net", "Password": "1990Chloe", "RememberMe": 0, "ToAppCode": "CONN"}
#
# content = sess.post(login_url, json=login_data)
# login_res = content.json().get("ErrMsg")
# if not login_res:
#     print("success")
#     with open("cookies.txt", "w+")as file:
#         file.write(json.dumps(sess.cookies.items()))
# else:
#     print(login_res)

# TIMEDICT = {"7 Days": "9", "14 Days": "10", "30 Days": "1", "45 Days": "11", "60 Days": "2", "90 Days": "3",
#             "1 Year": "4"}
#
# st = "7 Days"
#
# with open("keywords.json", "r+", encoding="utf-8")as f:
#     keywords_dict = json.loads(f.read())
#
# drpDays = TIMEDICT.get(st)
# keywords = "ALBUMS"
# drpProdLine = keywords_dict.get(keywords)
# baseUrl = "https://connect.asicentral.com/CreditReport/CRProfile?ID=119732&Source=MonitorDetail"
#
# data = ['asi/204120', 'https://connect.asicentral.com/MonitorDetailReport/Index/QuickView?pageID=ML&companyId=119732', 'General Promotions', 'Grosse Pointe Farms', 'MI', 'N/A']
# response = session.get(baseUrl).text
# print(response)
with open("html.html", "r+", encoding="utf-8")as f:
    response = f.read()
html = etree.HTML(response)


# mailing_address = re.findall(r'<div class="txtLabel text14">Mailing Address</div>([\s\S]*?)<div class="txtLabel text14">', response, re.M)
# if mailing_address:
#     mailingAddress = re.sub(r"(<.*?>)|(&nbsp;)|(N/A)", "", mailing_address[0]).strip()
# else:
#     mailingAddress = ""
# print(mailingAddress)
#
# delivery_address = re.findall(r'<div class="txtLabel text14">Delivery Address</div>([\s\S]*?)<div class="txtLabel text14">', response, re.M)
# if delivery_address:
#     deliveryAddress = re.sub(r"(<.*?>)|(&nbsp;)|(N/A)", "", delivery_address[0]).strip()
# else:
#     deliveryAddress = ""
# print(deliveryAddress)

company_executives = re.findall(r'<div class="txtLabel text14">Company Executives</div>([\s\S]*?)<div class="span3">', response, re.M)
if company_executives:
    companyExecutives = re.sub(r"(&nbsp;)|(<span.*?/span>)|(<.*?>)|(N/A)", "", company_executives[0]).strip()
else:
    companyExecutives = ""
print(companyExecutives)

phone = re.findall(r'<span class="txtLabel">Phone: </span>([\s\S]*?)</div>', response, re.M)
if phone:
    phoneNo = re.sub(r"(&nbsp;)|(<span.*?/span>)|(<.*?>)|(N/A)", "", phone[0]).strip()
else:
    phoneNo = ""
print(phoneNo)

email = re.findall(r'<span class="txtLabel">E-mail: </span>([\s\S]*?)</div>', response, re.M)
if email:
    emailTxt = re.sub(r"(&nbsp;)|(<span.*?/span>)|(<.*?>)|(N/A)", "", email[0]).strip()
else:
    emailTxt = ""
print(emailTxt)

web = re.findall(r'<span class="txtLabel">Web: </span>([\s\S]*?)</div>', response, re.M)
if web:
    webTxt = re.sub(r"(&nbsp;)|(<span.*?/span>)|(<.*?>)|(N/A)", "", web[0]).strip()
else:
    webTxt = ""
print(webTxt)

url = "/QuickView/QuickView?pageID=ML&companyId=119732"
print(re.findall(r"companyId=(.*)", url))
# search_data = []
# for lab_tr in html.xpath("//*[@id='tblMonitorList']/tbody/tr"):
#     search_data.append([
#         lab_tr.xpath("td[1]/a/span[@class='asi']/text()")[0],
#         "https://connect.asicentral.com/MonitorDetailReport/Index/{}".format(lab_tr.xpath("td[1]/a/@data-url")[0]),
#         lab_tr.xpath("td[2]/div/a/text()")[0],
#         lab_tr.xpath("td[3]/div/text()")[0],
#         lab_tr.xpath("td[4]/div/text()")[0],
#         lab_tr.xpath("td[5]/div/text()")[0]
#     ])
# print(search_data)







