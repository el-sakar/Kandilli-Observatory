import abc


class IUrlService(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def get_data(self): pass


class IParseService(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def get_data(self): pass


class ITransformService(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def get_data(self): pass
