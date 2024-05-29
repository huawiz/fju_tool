from src import coursedata
import datetime

current_time = datetime.datetime.now()
data = coursedata.getjsonCourseData()
print(coursedata.getNextCourse(data,current_time))
