

import sys
import abc
sys.path.append("..")
from utils.checkerror import log_debug, log_error



class IUrlService(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def get_data(self): pass

    def __str__(self):
        return log_debug("Url Service -- Healthy")


class IParseService(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def get_data(self): pass

    def __str__(self):
        return log_debug("Parse Service -- Healthy")


class ITransformService(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def get_data(self): pass

    def __str__(self):
        return log_debug("Transformation Service -- Healthy")

