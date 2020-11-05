import aiohttp
import asyncio
import json
import requests
from mttkinter import mtTkinter as mtk
import pickle
import threading
from tkinter.messagebox import *
from tkinter import ttk, Frame, scrolledtext, filedialog
import os
import re
from lxml import etree
import random
from datetime import datetime
from openpyxl import Workbook


PDFPATH = os.path.join(os.path.expanduser("~"), 'Desktop').replace("\\", "/")

FILEPATH = os.path.join(os.path.expanduser("~"), 'Connect').replace("\\", "/")
if not os.path.exists(FILEPATH):
    os.makedirs(FILEPATH)

SESSION_FILE_PATH = f"{FILEPATH}/session.pkl"
KEYWORDS_FILE_PATH = F"{FILEPATH}/keywords.json"
TIMEDICT = {"7 Days": "9", "14 Days": "10", "30 Days": "1", "45 Days": "11", "60 Days": "2", "90 Days": "3",
            "1 Year": "4"}


class LoginPage(object):
    def __init__(self, master=None):
        self.root = master
        self.root.geometry('%dx%d' % (450, 350))
        self.createPage()

    def createPage(self):
        self.login = mtk.LabelFrame(self.root, text="登录", fg="blue")
        self.login.place(x=30, y=50, width=380, height=250)

        self.label_asino = mtk.Label(self.login, text="AsiNumber：")
        self.label_asino.place(x=30, y=10, width=75, height=25)
        self.entry_asino = mtk.Entry(self.login)
        self.entry_asino.place(x=120, y=10, width=220, height=25)

        self.label_user = mtk.Label(self.login, text="账号：")
        self.label_user.place(x=30, y=65, width=75, height=25)
        self.entry_user = mtk.Entry(self.login)
        self.entry_user.place(x=120, y=65, width=220, height=25)

        self.label_passwd = mtk.Label(self.login, text="密码：")
        self.label_passwd.place(x=30, y=120, width=75, height=25)
        self.entry_passwd = mtk.Entry(self.login, show="*")
        self.entry_passwd.place(x=120, y=120, width=220, height=25)

        self.btn_logins = mtk.Button(self.login, text="自动登录", command=lambda: self.thread_it(self.loginSelf))
        self.btn_logins.place(x=40, y=170, width=100, height=30)

        self.btn_login = mtk.Button(self.login, text="登录", command=lambda: self.thread_it(self.loginContent))
        self.btn_login.place(x=220, y=170, width=100, height=30)

    def __loadSession(self):
        if os.path.exists(SESSION_FILE_PATH):
            with open(SESSION_FILE_PATH, "rb")as file1:
                info = pickle.load(file1)
                sess = info.get("session")
            check_res = self.__loginCheck(sess)
            if check_res:
                return sess
            return False

        return False

    def __loginCheck(self, sess):
        response = sess.get("https://connect.asicentral.com/Home")
        check = re.findall(r'<li class="welcometxt">Hello, (.*?)</li>', response.text)
        if check:
            return True
        return False

    def loginSelf(self):
        lod_res = self.__loadSession()
        if lod_res:
            sess = lod_res
            self.login.destroy()
            MainPage(sess, master=self.root)

        else:
            showerror("Error Info", "登录失效, 请重新登录!")

    def loginContent(self):
        sess = requests.Session()
        sess.headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'referer': 'https://connect.asicentral.com/login?401',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'
        }

        asinumber = self.entry_asino.get().strip()
        if not asinumber:
            showerror("Error Info", "请输入Asi Number!")
            return

        loginname = self.entry_user.get().strip()
        if not loginname:
            showerror("Error Info", "账号不能为空!")
            return

        loginpwd = self.entry_passwd.get().strip()
        if not loginpwd:
            showerror("Error Info", "请输入密码!")
            return

        login_url = "https://connect.asicentral.com/Login//Home/LoginUser"
        login_data = {"AsiNumber": asinumber, "UserName": loginname, "Password": loginpwd, "RememberMe": 0, "ToAppCode": "CONN"}

        response = sess.post(login_url, json=login_data)
        login_res = response.json().get("ErrMsg")
        if login_res:
            showerror("Error Info", "登录失败, 请检查账号密码!")
            return

        showinfo("OK", "登录成功!")
        with open(SESSION_FILE_PATH, "wb")as f:
            info = {"session": sess}
            pickle.dump(info, f)
        self.login.destroy()
        MainPage(sess, master=self.root)

    @staticmethod
    def thread_it(func, *args):
        t = threading.Thread(target=func, args=args)
        t.setDaemon(True)
        t.start()


class InputFrame(Frame):
    def __init__(self, session, master=None):
        super(InputFrame, self).__init__()
        self.root = master
        self.session = session
        self.root.geometry('600x500')
        self.root.title("Connect")
        self.createPage()
        self.excelData = [["ASINumber", "DistributorName", "City", "State", "CreditScore", "CompanyExecutive", "Phone", "Email", "Web"]]
        with open(KEYWORDS_FILE_PATH, "r+", encoding="utf-8")as file:
            self.keywords_dict = json.loads(file.read())

    def createPage(self):
        self.infoBox = mtk.LabelFrame(self.root, text="搜索框", fg="blue")
        self.infoBox.place(x=20, y=20, width=540, height=100)

        self.kw = mtk.Label(self.infoBox, text="关键词：")
        self.kw.place(x=20, y=20, width=50, height=25)
        self.kwText = mtk.Entry(self.infoBox)
        self.kwText.place(x=80, y=20, width=150, height=25)

        self.searchTime = mtk.Label(self.infoBox, text="搜索时间：")
        self.searchTime.place(x=280, y=20, width=60, height=25)
        self.stText = ttk.Combobox(self.infoBox)
        self.stText.place(x=350, y=20, width=100, height=25)
        self.stText["values"] = ["7 Days", "14 Days", "30 Days", "45 Days", "60 Days", "90 Days", "1 Year"]

        self.log = mtk.LabelFrame(self.root, text="log日志", fg="blue")
        self.log.place(x=20, y=140, width=300, height=350)
        self.logtext = scrolledtext.ScrolledText(self.log, fg="green")
        self.logtext.place(x=20, y=15, width=270, height=300)

        self.status = mtk.LabelFrame(self.root, text="当前进度", fg="blue")
        self.status.place(x=340, y=140, width=220, height=150)

        self.indexnow = mtk.Label(self.status, text="当前条数：")
        self.indexnow.place(x=20, y=20, width=60, height=25)
        self.indexnowText = mtk.Label(self.status, text="0 条")
        self.indexnowText.place(x=90, y=20, width=50, height=25)

        self.indexTotals = mtk.Label(self.status, text="总条数：")
        self.indexTotals.place(x=20, y=65, width=60, height=25)
        self.indexTotalsText = mtk.Label(self.status, text="0 条")
        self.indexTotalsText.place(x=90, y=65, width=50, height=25)

        self.btnBox = mtk.LabelFrame(self.root)
        self.btnBox.place(x=340, y=320, width=220, height=170)

        self.startbtn = mtk.Button(self.btnBox, text="开始", command=lambda: self.thread_it(self.start))
        self.startbtn.place(x=40, y=20, width=120, height=40)
        self.loadoutbtn = mtk.Button(self.btnBox, text="导出", command=lambda: self.thread_it(self.export))
        self.loadoutbtn.place(x=40, y=100, width=120, height=40)

    def export(self):
        if len(self.excelData) <= 1:
            showerror("错误信息", "当前不存在任何数据!")
            return

        excelPath = filedialog.asksaveasfilename(title=u'保存文件', filetypes=[("xlsx", ".xlsx")]) + ".xlsx"
        if excelPath.strip(".xlsx"):
            wb = Workbook()
            ws = wb.active
            for line in self.excelData:
                ws.append(line)
            wb.save(excelPath)
            showinfo("提示信息", "保存成功！")

    def searchKeywords(self):
        keywords = self.kwText.get().strip().upper()
        if not keywords:
            showerror("Error Info", "请输入关键词!")
            return

        st = self.stText.get().strip()
        if not st:
            showerror("Error Info", "请输入搜索时间!")
            return

        drpProdLine = self.keywords_dict.get(keywords)
        if not drpProdLine:
            showerror("Error Info", "关键词输入错误!")
            return
        self.logtext.insert(mtk.END,f"{datetime.now().strftime('%H:%M:%S')}\t当前搜索关键词：{keywords}.\n")

        drpDays = TIMEDICT.get(st)
        baseUrl = f"https://connect.asicentral.com/Search/SearchResults?txtCompanyName=&chkBranches=false&txtExecutiveName=&txtPhone=&txtDistributorLocation=&drpState=&txtZip=&txtStartingZip=&drpRange=&drpProdLine={drpProdLine}&drpDays={drpDays}&txtPriceFrom=&txtPriceTo=&txtFullTimeFrom=&txtFullTimeTo=&txtSalesFrom=&txtSalesTo=&txtPartTimeFrom=&txtPartTimeTo=&drpAvgPayHabitFrom=&drpAvgPayHabitTo=&drpProductLinesH=9&drpCustomerType=&chkTop40=false&chkCanadian=false&chkApparel=false"

        response = self.session.get(baseUrl).text
        html = etree.HTML(response)
        totalsNum = html.xpath("//div[@class='span']/strong[1]/text()")
        if totalsNum:
            totalsNum = totalsNum[0]
        else:
            totalsNum = "0"
        self.indexTotalsText.configure(text=totalsNum + "条")
        self.logtext.insert(mtk.END, f"{datetime.now().strftime('%H:%M:%S')}\t共搜索到{totalsNum}条数据.\n")
        if totalsNum == "0":
            return []
        search_data = []
        for lab_tr in html.xpath("//*[@id='tblMonitorList']/tbody/tr"):
            search_data.append([
                lab_tr.xpath("td[1]/a/span[@class='asi']/text()")[0].replace("asi/", ""),
                "https://connect.asicentral.com/CreditReport/CRProfile?ID={}&Source=MonitorDetail".format(re.findall(r"companyId=(.*)", lab_tr.xpath("td[1]/a/@data-url")[0])[0]),
                lab_tr.xpath("td[2]/div/a/text()")[0] if lab_tr.xpath("td[2]/div/a/text()") else "",
                lab_tr.xpath("td[3]/div/text()")[0] if lab_tr.xpath("td[3]/div/text()") else "",
                lab_tr.xpath("td[4]/div/text()")[0] if lab_tr.xpath("td[4]/div/text()") else "",
                lab_tr.xpath("td[5]/div/text()")[0] if lab_tr.xpath("td[5]/div/text()") else ""
            ])
        return search_data

    async def getDdetail(self, semaphore, itemData):
        async with semaphore:
            conn = aiohttp.TCPConnector(verify_ssl=False)
            cookies = "".join([f"{name}={value};" for name, value in self.session.cookies.items()])
            headers = {
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'accept-encoding': 'gzip, deflate, br',
                'accept-language': 'zh-CN,zh;q=0.9',
                'cookie': cookies,
                'sec-fetch-dest': 'document',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-site': 'same-origin',
                'sec-fetch-user': '?1',
                'upgrade-insecure-requests': '1',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'
            }
            async with aiohttp.ClientSession(connector=conn, headers=headers) as session:
                try:
                    link = itemData.pop(1)
                    async with await session.get(link, timeout=300) as resp:
                        content = await resp.text()
                        await asyncio.sleep(random.uniform(0, 3))
                        return itemData, content
                except Exception as e:
                    print(e.args)
                    return

    def detailItem(self, feature):
        self.index += 1
        itemData, htmlText = feature.result()
        company_executives = re.findall(
            r'<div class="txtLabel text14">Company Executives</div>([\s\S]*?)<div class="span3">', htmlText, re.M)
        if company_executives:
            companyExecutives = re.sub(r"(&nbsp;)|(<span.*?/span>)|(<.*?>)|(N/A)", "", company_executives[0]).strip().split("\n")[0].strip()
        else:
            companyExecutives = ""
        itemData.append(companyExecutives)

        phone = re.findall(r'<span class="txtLabel">Phone: </span>([\s\S]*?)</div>', htmlText, re.M)
        if phone:
            phoneNo = re.sub(r"(&nbsp;)|(<span.*?/span>)|(<.*?>)|(N/A)", "", phone[0]).strip()
        else:
            phoneNo = ""
        itemData.append(phoneNo)

        email = re.findall(r'<span class="txtLabel">E-mail: </span>([\s\S]*?)</div>', htmlText, re.M)
        if email:
            emailTxt = re.sub(r"(&nbsp;)|(<span.*?/span>)|(<.*?>)|(N/A)", "", email[0]).strip()
        else:
            emailTxt = ""
        itemData.append(emailTxt)

        web = re.findall(r'<span class="txtLabel">Web: </span>([\s\S]*?)</div>', htmlText, re.M)
        if web:
            webTxt = re.sub(r"(&nbsp;)|(<span.*?/span>)|(<.*?>)|(N/A)", "", web[0]).strip()
        else:
            webTxt = ""
        itemData.append(webTxt)
        if itemData not in self.excelData and emailTxt:
            self.excelData.append(itemData)
        else:
            self.dupindex += 1
        self.indexnowText.configure(text=str(self.index) + "条")

    async def taskManager(self, dataItemList, func):
        tasks = []
        sem = asyncio.Semaphore(4)
        for itemData in dataItemList:
            task = asyncio.ensure_future(func(sem, itemData))
            task.add_done_callback(self.detailItem)
            tasks.append(task)
        await asyncio.gather(*tasks)

    def start(self):
        self.index = 0
        self.dupindex = 0
        dataItemList = self.searchKeywords()
        if dataItemList:
            self.logtext.insert(mtk.END, f"{datetime.now().strftime('%H:%M:%S')}\t开始任务,请勿关闭程序.\n")
            new_loop = asyncio.new_event_loop()
            asyncio.set_event_loop(new_loop)
            self.loop = asyncio.get_event_loop()
            self.loop.run_until_complete(self.taskManager(dataItemList, self.getDdetail))
            self.logtext.insert(mtk.END, f"{datetime.now().strftime('%H:%M:%S')}\t数据获取任务结束(共剔除{self.dupindex}条无邮箱数据或重复数据).\n")

    @staticmethod
    def thread_it(func, *args):
        t = threading.Thread(target=func, args=args)
        t.setDaemon(True)
        t.start()

class MainPage(object):
    def __init__(self, cookies, master=None):
        self.root = master
        self.root.geometry('%dx%d' % (600, 500))
        self.createPage(cookies)

    def createPage(self, cookies):
        self.inputPage = InputFrame(cookies, self.root)
        self.inputPage.pack()

    def inputData(self):
        self.inputPage.pack()


if __name__ == '__main__':
    root = mtk.Tk()
    root.title('登录')
    LoginPage(root)
    root.mainloop()
