

from datetime import datetime as dt


def datetime_converter(value):
    """ Convert the datetime """
    oldformat = [ x for x in value if not x == '.']
    oldformat = ''.join(map(str,oldformat))
    datetime_obj = dt.strptime(oldformat, '%Y%m%d')
    newformat = datetime_obj.strftime('%Y-%m-%d')
    return newformat

