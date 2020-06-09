#!/usr/bin/env python3
# -*-coding=utf-8-*-

# __author= "Emrah Burak Gürbüz"
# Uncomment the next line to see my email
# print(bytes.fromhex("67656d726168627572616b40676d61696c2e636f6d").decode("utf-8"))
#
# __licence__ = """This program name is observatory.py. You can parse data from Kandilli Observatory/Turkey
#     Copyright (C) 2019  """+__author+ """
#
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <https://www.gnu.org/licenses/>."""
try:
    import requests
    import os
    import json
    import csv
    import re
    # import numpy as np
    from bs4 import BeautifulSoup
    from datetime import datetime as dt
except Exception as err:
    print(err)


class GetBase():
    def __init__(self):
        self.f = dt.now().strftime('%Y%m%d')
        self.f_2 = str(dt.now().hour)+str(dt.now().minute)+str(dt.now().second)
        self.mixed_f = self.f + '_' + self.f_2
        self.file_name_csv = self.mixed_f + '.csv'
        self.file_name_json = self.mixed_f + '.json'
        self.BASE_DIR = os.getcwd()
        self.dirname = 'observatory'
        self.check_file = os.path.exists
        self.dateregex = '[0-9]+[.]+'
        self.timeregex = '[0-9]+[:]+'
        self.check_ilksel = ['ilksel']
        self.dict_box = []
        self.collector = []
        self.counter_numline = []
        self._error = True
        self.float_base = 0.0
        self.float_oldbase = ['-.-']
        self.cols = ('tarih', 'saat', 'enlem',
                     'boylam', 'derinlikkm',
                     'md', 'ml', 'mw', 'yer',
                     'cozumniteligi')

        # specify the URL of the archive here ***
        self.archive_url = "http://www.koeri.boun.edu.tr/scripts/lst2.asp"
        # ***

class GetLink(GetBase):
    def __init__(self):
        super(GetLink, self).__init__()
        self.get_data = ''
        self.main_dict = {}

    def get_txt_links(self):
        try:
            self.r = requests.get(self.archive_url)

            # create beautiful-soup object
            self.soup = BeautifulSoup(self.r.content, 'html5lib')
            # or
            # soup = BeautifulSoup(r.content, 'html.parser')

            # find all links on web-page
            # self.text = self.soup.get_text()
            self.pre = self.soup.find_all('pre')[-1]
            self.get_text = self.pre.text

            for num_getText, i in enumerate(self.get_text.splitlines()[6:]):
                # print(num_getText, i)
                self.get_data += i + '\n'

            # print("end of lines: ",self.get_data.splitlines()[-1:])
            self.get_data = self.get_data[:-1]
        except Exception as err:
            print(err)
            self._error = False
        finally:
            if self._error:
                return self.link_parsing()
                # return self.get_data

    def link_parsing(self):
        try:
            for num_line, line in enumerate(self.get_data.splitlines()):
                self.dict = {}
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
                # self.matrix_ilksel = np.array(
                #     [z for z in self.matrix_base[8:] if z in self.matrix_base[-1] and re.match('^.*[a-z]', z)])
                self.matrix_ilksel = self.list_ilksel


                # print(self.list_ilksel)



                
                if self.matrix_col_eight:
                    self.dict[self.cols[8]] = ''.join(map(str, self.matrix_col_eight))

                if self.matrix_revize or self.matrix_revize_date or self.matrix_revize_time:
                    self.dict[self.cols[9]] = self.matrix_revize[0] + '' + self.matrix_revize_date[0] + '-' + \
                        self.matrix_revize_time[0]

                # if self.matrix_ilksel.size > 0:
                if len(self.matrix_ilksel) > 0:
                    self.dict[self.cols[9]] = self.matrix_ilksel[0]


                # # convert datetime form 
                # self.dict['tarih'] = datetime_converter(self.dict['tarih'])
                self.dict_box.append(self.dict)







            
        except (Exception) as error:
            print(error)
            self._error = False
            return -1
        finally:
            if self._error:
                if self.dict_box:
                    # print(self.dict_box)

                    return self.dict_box



                    # +++++++Check your data+++++++
                    # for num, i in enumerate(self.dict_box):
                    #     print(num, i)





class GetDataJSON(GetBase):
    def __init__(self):
        super(GetDataJSON, self).__init__()
        self.data = GetLink().get_txt_links()
        # print(self.data)

    def create(self):
        try:
            if self.data:
                ishere = os.path.exists(self.dirname)
                if ishere:
                    pass
                else:
                    os.mkdir(self.dirname)

                self.join_with = os.path.join(self.BASE_DIR, self.dirname, self.file_name_json)
                with open(self.join_with, 'w') as write_json:
                    if self.data:
                        json.dump(self.data,write_json,ensure_ascii=False,indent=4)

        except Exception as error:
            print(error)
            self._error = False
            return -1


        finally:
            try:
                write_json.close()
                if self._error and self.check_file(self.join_with):
                    self.messageTr = 'Dosya: ' + self.join_with + ' konumuna  yazıldı.'
                    self.messageEn = 'File: created to ' + self.join_with
                    print(self.messageTr)
                    print(self.messageEn)
                    return 0
            except (Exception) as error:
                print(error)



class GetDataCSV(GetBase):
    def __init__(self):
        super(GetDataCSV, self).__init__()
        self.dict_data = GetLink().get_txt_links()
        pass

    def create(self):
        try:
            if self.dict_data:
                ishere = os.path.exists(self.dirname)
                if ishere:
                    pass
                else:
                    os.mkdir(self.dirname)

                self.join_with = os.path.join(self.BASE_DIR, self.dirname, self.file_name_csv)
                with open(self.join_with, 'w') as write_csv:
                    writer = csv.DictWriter(write_csv, fieldnames=self.cols)
                    writer.writeheader()
                    for data in self.dict_data:
                        writer.writerow(data)

        except Exception as error:
            print(error)
            self._error = False
            return -1


        finally:
            write_csv.close()
            if self._error and self.check_file(self.join_with):
                self.messageTr = 'Dosya: ' + self.join_with + ' konumuna  yazıldı.'
                self.messageEn = 'File: created to '+ self.join_with
                print(self.messageTr)
                print(self.messageEn)
                return 0



class ObservatoryManager():
    def __init__(self, file_strategy):
        self.file_strategy = file_strategy
        self.create()

    def create(self):
        self.file_strategy.create()


if __name__ == '__main__':
    app = ObservatoryManager(GetDataCSV())
    # app = ObservatoryManager(GetDataJSON())
