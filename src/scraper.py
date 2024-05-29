import requests
from lxml import html
from bs4 import BeautifulSoup as bs
import json
import os

class CourseData:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def get_request(self):
        # 建立連線
        session_requests = requests.session()
        result = session_requests.get('http://estu.fju.edu.tw/CheckSelList/HisListNew.aspx')
        tree = html.fromstring(result.text)

        # 登入學校網站所需Header資料
        headers = {
            'Connection': 'keep-alive',
            'Content-Length': '593',
            'Cache-Control': 'max-age=0',
            'Origin': 'http://estu.fju.edu.tw',
            'Upgrade-Insecure-Requests': '1',
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Referer': 'http://estu.fju.edu.tw/CheckSelList/HisListNew.aspx',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-TW,zh;q=0.9',
            }


        # 獲取登入學校課表網站所需的payload資料
        __VIEWSTATE = list(set(tree.xpath('//input[@name="__VIEWSTATE"]/@value')))[0]
        __VIEWSTATEGENERATOR = list(set(tree.xpath('//input[@name="__VIEWSTATEGENERATOR"]/@value')))[0]
        __EVENTVALIDATION = list(set(tree.xpath('//input[@name="__EVENTVALIDATION"]/@value')))[0]

        # payload 資料
        payload = {
            '__VIEWSTATE': __VIEWSTATE,
            '__VIEWSTATEGENERATOR': __VIEWSTATEGENERATOR,
            '__EVENTVALIDATION': __EVENTVALIDATION,
            'ButLogin': '登入',
            'TxtLdapId': self.username,
            'TxtLdapPwd': self.password
        }

        # post 資料，並獲取網頁資料
        result = session_requests.post('http://estu.fju.edu.tw/CheckSelList/HisListNew.aspx', data = payload, headers = headers)

        # 關閉連線
        session_requests.close()
        return result.text
        
    def CourseData(self, request_text):

        # 取得beautifulsoup物件，並使用html解析器
        soup = bs(request_text, 'html.parser')

        # 取得課表標頭，取前17欄的標頭，只包含正課
        heads = soup.select("#GV_NewSellist th")
        head_list = [head.text.strip() for head in heads[:17]]

        # 取得課表資料，取前17欄的資料
        rows = soup.select("#GV_NewSellist > tr")
        row_list = []
        for row in rows[:17]:
            col_list = []
            cols = row.find_all("td",recursive=False)
            for col in cols[:17]:
                col_list.append(col.text.strip())
            row_list.append(col_list)

        # 去除第一筆空值
        row_list = row_list[1:]

        # mapping 標頭與課程資料，若無資料則回傳空值
        course = [dict(zip(head_list, row)) for row in row_list] if row_list else None
        return course

    def saveData(self, data):
        module_dir = os.path.dirname(os.path.abspath(__file__))
        project_dir = os.path.dirname(module_dir)
        data_dir = os.path.join(project_dir, 'data')
        file_path = os.path.join(data_dir, 'courseData.json')
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)

        file_path = os.path.join(data_dir, 'courseData.json')

        # 将数据写入文件
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

def updateCourse(username,password):
    stu = CourseData(username,password)
    request = stu.get_request()
    stu.saveData(stu.CourseData(request))




    


