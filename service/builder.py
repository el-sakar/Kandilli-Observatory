
import abc
from parse import Parse
from json_service import JsonService
from csv_service import CsvService
from url_service import UrlServiceImpl



class IBuilder(metaclass=abc.ABCMeta):
    "interface"

    @abc.abstractmethod
    def with_url(self, value): pass

    @abc.abstractmethod
    def with_parse(self): pass

    @abc.abstractmethod
    def with_json(self): pass

    @abc.abstractmethod
    def with_csv(self): pass

    @abc.abstractmethod
    def with_close(self): pass


class Builder(IBuilder):

    def __init__(self):
        self.result = Result()

    def with_url(self, url):
        "do something"
        self.parseable = UrlServiceImpl(url).get_data()
        assert(self.parseable != True),"with_url in error"
        return self

    def with_parse(self):
        "parse data from url"
        print(Parse())
        return self

    def with_json(self):
        "transform data as json"
        print(JsonService())
        return self

    def with_csv(self):
        "transform data as csv"
        print(CsvService())
        return self

    def with_close(self):
        print("with close working")


class Result():
    "Result clean data"

    def __init__(self):
        print("Result will be created")



def main():

    archive_url = "http://www.koeri.boun.edu.tr/scripts/lst2.asp"
    builder = Builder()
    builder.with_url(archive_url).with_parse(
    ).with_json().with_close()


if __name__ == "__main__":
    main()
