
import sys
import re
from services import IParseService
sys.path.append("..")
from utils.checkerror import log_debug, log_error
from utils.converters import datetime_converter



class ParseServiceImpl(IParseService):


    def __init__(self, parseable=None):
        self.parseable = parseable
        self.counter_numline = []
        self.cols = ('tarih', 'saat', 'enlem',
                     'boylam', 'derinlikkm',
                     'md', 'ml', 'mw', 'yer',
                     'cozumniteligi')

        self.float_base = 0.0
        self.float_oldbase = ['-.-']
        self.dict = {}
        self.dateregex = '[0-9]+[.]+'
        self.timeregex = '[0-9]+[:]+'
        self.check_ilksel = ['ilksel']
        self.dict_box = []
        self._error = True

    def get_data(self):
        "parse string data to dictionary"
        try:
            for num_line, line in enumerate(self.parseable.splitlines()):
                self.counter_numline.append(num_line)
                self.matrix_base = line.split()
                # self.list_base = line.split()
                # assert(self.matrix_base == self.list_base, "Get A problem")
                
                for dict_index in range(len(self.cols[:5])):
                    self.dict[self.cols[dict_index]] = self.matrix_base[dict_index]

                if self.matrix_base[5] in self.float_oldbase:
                    self.dict[self.cols[5]] = self.float_base

                else:
                    self.dict[self.cols[5]] = self.matrix_base[5]

                if self.matrix_base[6] in self.float_oldbase:
                    self.dict[self.cols[6]] = self.float_base

                else:
                    self.dict[self.cols[6]] = self.matrix_base[6]

                if self.matrix_base[7] in self.float_oldbase:
                    self.dict[self.cols[7]] = self.float_base

                else:
                    self.dict[self.cols[7]] = self.matrix_base[7]

                self.matrix_col_eight = [x for x in self.matrix_base[8:] if x.isupper()]
                self.matrix_revize = [y for y in self.matrix_base[8:] if re.search("[A-Z]+[0-9]+", y)]
                self.matrix_revize_date = [p for p in self.matrix_base[8:] if re.search(self.dateregex, p)]
                self.matrix_revize_time = [k for k in self.matrix_base[8:] if re.match(self.timeregex, k)]
                self.list_ilksel = [z for z in self.matrix_base[8:] if z in self.matrix_base[-1] and re.match('^.*[a-z]', z)]
                self.matrix_ilksel = self.list_ilksel

                if self.matrix_col_eight:
                    self.dict[self.cols[8]] = ''.join(map(str, self.matrix_col_eight))

                if self.matrix_revize or self.matrix_revize_date or self.matrix_revize_time:
                    self.dict[self.cols[9]] = self.matrix_revize[0] + '' + self.matrix_revize_date[0] + '-' + \
                        self.matrix_revize_time[0]

                if len(self.matrix_ilksel) > 0:
                    self.dict[self.cols[9]] = self.matrix_ilksel[0]

                # convert datetime form via datetime_converter 
                self.dict['tarih'] = datetime_converter(self.dict['tarih'])
                self.dict_box.append(self.dict)

        except (Exception) as error:
            self._error = log_error(error)
            return -1
        finally:
            if self._error:
                if self.dict_box:
                    #Test
                    #print(self.dict_box)
                    return self._error, self.dict_box, self.__str__()


