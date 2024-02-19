import os
import time
import datetime

def getExpiresTime(filepath):
    """
        > 获取cookies文件的修改时间
          https://developer.aliyun.com/article/891516
          https://cloud.tencent.com/developer/article/1703305
          看文件里到期时间是2天，所以修改时间+2d 和现在时间做比较
        > time对象和datetime对象转换
          https://blog.csdn.net/qq_36523839/article/details/107394697
          https://blog.csdn.net/u010591976/article/details/104271196
    """
    # cookies txt最后一次修改时间, st_mtime是1668410923.5456736，int一下拿秒级时间戳
    cookiesModTime = time.localtime(int(os.stat(filepath).st_mtime))
    strfModTime = time.strftime("%Y-%m-%d %H:%M:%S", cookiesModTime)
    datetimeCookiesModTime = datetime.datetime.strptime(strfModTime, "%Y-%m-%d %H:%M:%S")
    # cookies_file 到期时间
    datetimeCookiesExpires = datetimeCookiesModTime + datetime.timedelta(days=2)

    return datetimeCookiesExpires

value = getModTime("../data/cookies.txt")
print(value)



def getValues(keyWord, data):
    if not isinstance(data, dict):
        return None

    if keyWord in data:
        return data[keyWord]

    for value in data.values():
        result = getValues(value, keyWord)
        if result is not None:
            return result

    return None


