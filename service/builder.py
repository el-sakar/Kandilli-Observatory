
import abc
from parse_service import ParseServiceImpl
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
        print(self.result)

    def with_url(self, url):
        "get dirty text data from url"

        #-----------------------------(err,data,className)--
        #self.parseable : type - tuple(bool,string,bool)
        self.parseable = UrlServiceImpl(url).get_data()
        self.parse_status = self.parseable[0]
        assert(self.parse_status == True),"URL Service -- Error"
        self.parseable_data = self.parseable[1]
        return self

    def with_parse(self):
        "parse data from url"

        self.clean = ParseServiceImpl(self.parseable_data).get_data()
        self.clean_status = self.clean[0]
        assert(self.clean_status == True), "Parse service -- Error"
        self.clean_data = self.clean[1]
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


    def __str__(self):
        return "Result will be create"



        

def main():
    "test "

    archive_url = "http://www.koeri.boun.edu.tr/scripts/lst2.asp"
    builder = Builder()
    builder.with_url(archive_url).with_parse().with_json().with_close()


if __name__ == "__main__":
    main()
