import datetime

def DateTimeToStr(pDateTime, format='%Y-%m-%d %H:%M:%S'):
    '''
    datetime转str
    :param pDateTime: datetime格式时间
    :param format: 时间格式
    :return: str
    '''
    if not isinstance(pDateTime, datetime.datetime):
        raise ValueError
    str = pDateTime.strftime(format)
    return str


def StrToDateTime(pStr, format='%Y-%m-%d %H:%M:%S'):
    '''
    str转datetime
    :param pStr: 字符串格式时间
    :param format: 时间格式
    :return: datetime
    '''
    if not isinstance(pStr, str):
        raise ValueError
    time = datetime.datetime.strptime(pStr, format)
    return time


def StrToTimestamp(pStr, format='%Y-%m-%d %H:%M:%S'):
    '''
    字符串转时间戳
    :param pStr: 字符串格式时间
    :param format: 时间格式
    :return: timestamp
    '''
    if not isinstance(pStr, str):
        raise ValueError
    timestamp = int(datetime.datetime.strptime(pStr, format).timestamp())
    return timestamp


def TimestampToStr(pTimestamp, format='%Y-%m-%d %H:%M:%S'):
    '''
    时间戳转字符串
    :param pTimestamp: 时间戳
    :param format: 时间格式
    :return: str
    '''
    str = datetime.datetime.fromtimestamp(float(pTimestamp)).strftime(format)
    return str