import datetime
import pytz
import json
from bs4 import BeautifulSoup
import os



# 共同變數
periods = ['D0', 'D1', 'D2', 'D3', 'D4', 'DN', 'D5', 'D6', 'D7', 'D8', 'E0', 'E1', 'E2', 'E3', 'E4']
periodMapping = {period: i for i, period in enumerate(periods)}

times = ['07:10', '08:10', '09:10', '10:10', '11:10', '12:40', '13:40', '14:40', '15:40', '16:40', '17:40', '18:40', '19:35', '20:30', '21:25']
dictMappingPeriodTime = {period: time for period, time in zip(periods, times)}

# 讀課表資料
def getjsonCourseData():
   # 获取当前文件所在的目录（即模块文件的目录）
    module_dir = os.path.dirname(os.path.abspath(__file__))
        
        # 获取项目的根目录
    project_dir = os.path.dirname(module_dir)

        # 拼接文件路径
    filePath = os.path.join(project_dir, 'data','courseData.json')
    
    # 確保目錄存在
    os.makedirs(os.path.dirname(filePath), exist_ok=True)
    
    # 嘗試打開並讀取檔案
    try:
        with open(filePath, 'r', encoding='utf-8') as f:
            jsonCourseData = json.load(f)
    except FileNotFoundError:
        # 如果檔案不存在，建立一個新的空檔案
        jsonCourseData = {}
        with open(filePath, 'w', encoding='utf-8') as f:
            json.dump(jsonCourseData, f, ensure_ascii=False, indent=4)
    
    return jsonCourseData

#獲得今天的Weekday index
def getIdxToday():
    timezoneTW = pytz.timezone('Asia/Taipei')
    return datetime.datetime.now(timezoneTW).weekday()

#獲取今日課表資料
def getTodayCourse(jsonCourseData):
    return getDayCourse(jsonCourseData,getIdxToday())


# 獲取指定日期課表資料
def getDayCourse(jsonCourseData, intWeekDay):
    weekdayMapping = {i: day for i, day in enumerate(["一", "二", "三", "四", "五", "六", "日"])}
    return [course for course in jsonCourseData if course['星期'] == weekdayMapping[intWeekDay]]

    
#下一個有課日
def getNextCourseDay():
    jsonCourseData = getjsonCourseData()
    idxToday = getIdxToday()
    for i in range(1, 8):
        idx = (idxToday + i) % 7
        if getDayCourse(jsonCourseData, idx):
            return idx
    return None



# 取得同天中，距離現在最近的下一堂課
def getNextPeriodCourse(todayCourses, timeCurrent):
    timeCurrentStr = timeCurrent.strftime('%H:%M')
    nextCourse = None
    minTimeDiff = float('inf')  # 初始設置一個極大值來存放最小時間差
    for course in todayCourses:
        courseTime = dictMappingPeriodTime.get(course['節次'].split('-')[0])  # 取得課程開始時間
        if courseTime:
            timeDiff = (datetime.datetime.strptime(courseTime, '%H:%M') - datetime.datetime.strptime(timeCurrentStr, '%H:%M')).total_seconds()
            # 如果時間差為負，表示課程已經開始，不考慮這個課程
            if timeDiff >= 0 and timeDiff < minTimeDiff:
                minTimeDiff = timeDiff
                nextCourse = course
    return nextCourse

# 取得下一堂課
def getNextCourse(jsonCourseData, timeCurrent):
    # 取得今天的課程
    todayCourses = getTodayCourse(jsonCourseData)
    
    # 如果今天有課程
    if len(todayCourses)!=0:
        # 找到下一個節次的課程
        nextCourse = getNextPeriodCourse(todayCourses, timeCurrent)
        if nextCourse:
            return nextCourse
    
    # 如果今天沒有課程或找不到下一個節次的課程，從明天開始找下一堂課
    nextCourseDay = getNextCourseDay()
    if nextCourseDay is not None:
        nextDayCoureSchedule = getDayCourse(jsonCourseData, nextCourseDay)
        if len(nextDayCoureSchedule):
            return nextDayCoureSchedule[0]
    
    # 如果還是找不到
    return None


# WebView使用


def getScheduleData(data):
    
    scheduleData = []

    # 對所有可能的星期進行處理
    for day in ["一", "二", "三", "四", "五", "六"]:
        # 初始化該天的課程列表
        daySchedule = (day, [])
        
        for course in data:
            if course["星期"] == day and course["節次"] != "-":
                time = course["節次"]
                courseName = course["科目名稱"]
                
                # 將節次的格式轉換為所需格式
                if "-" in time:
                    start, end = time.split("-")
                    start = periodMapping[start]
                    end = periodMapping[end]
                    timeRange = f"{start}-{end}"
                else:
                    timeRange = periodMapping[int(time)]
                
                # 將課程添加到該天的課程列表中
                daySchedule[1].append((timeRange, courseName))
        
        # 添加該天的課程列表到 scheduleData 中
        scheduleData.append(daySchedule)
    return scheduleData

# 合併每欄垂直的表格
def mergeSameRowHtml(htmlContent):
    # 使用 BeautifulSoup 解析 HTML
    soup = BeautifulSoup(htmlContent, 'html.parser')
    # 第一個<tr>為標頭，因此從第二列開始處理
    trs = soup.find_all('tr')[1:]
    # 從週一到週六，一欄一欄處理垂直<td>標籤
    for weekday in range(6):  
        rowspan = 1
        # 基準列，和此列之後的next_row比對資料
        for row in range(len(trs)):
            tds = trs[row].find_all('td')
            # 設定基準列
            currentCell = tds[weekday]
            for next_row in range(row + 1, len(trs)):
                nextTds = trs[next_row].find_all('td')
                # 檢查內容
                if nextTds[weekday].get_text() == currentCell.get_text() :
                    # 如果有內容一致，則在第一個之後的標籤，給予kill屬性，全部標註完成後再刪除
                    nextTds[weekday]['kill'] = '1'
                    # 每檢查到一個相同的內容，基準列的rowspan屬性+1
                    rowspan += 1
                    currentCell['rowspan'] = rowspan
                else:
                    # 若下一個和基準不一樣，則跳出迴圈，重置rowspan數為1
                    rowspan = 1
                    break
                    
    # 刪除所有有屬性 'kill'='1' 的標籤
    for tag in soup.find_all(attrs={"kill": "1"}):
        tag.decompose()
    # 將修改後的 HTML 內容轉換為字串
    modifiedHtml = soup.prettify()
    return modifiedHtml
'''
# 渲染課表HTML
def renderCourse():
    render = render_template('course.html',courseName = '課表',periodMapping=periodMapping,scheduleData=getScheduleData(getjsonCourseData()))
    render = mergeSameRowHtml(render)
    return render
'''
            

            