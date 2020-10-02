
import sys
import requests
from bs4 import BeautifulSoup
from services import IUrlService
sys.path.append("..")
from utils.checkerror import log_debug, log_error




class UrlServiceImpl(IUrlService):

    def __init__(self, url):
        self.url = url
        self.result_data = ""
        self._error = True

    def get_data(self):
        """create beautiful-soup object
            find all pre on web-page
            get text """
        try:
            self.r = requests.get(self.url)
            if self.r.status_code == 200:
                self.soup = BeautifulSoup(self.r.content, 'html5lib')
                self.pre = self.soup.find_all('pre')[-1]
                self.get_text = self.pre.text
                for num_getText, i in enumerate(self.get_text.splitlines()[6:]):
                    self.result_data += i + '\n'

                    self.result_data = self.result_data[:-1]
        except Exception as err:
            self._error = log_error(err)
            return self._error
        finally:
            return self._error, self.result_data, self.__str__()


