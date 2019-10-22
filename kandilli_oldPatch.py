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

import requests
import os
import json
import csv
from bs4 import BeautifulSoup
from datetime import datetime as dt


class GetBase():
    def __init__(self):
        self.f = dt.now().strftime('%Y%m%d')
        self.f_2 = str(dt.now().hour)+str(dt.now().minute)+str(dt.now().second)
        self.mixed_f = self.f + '_' + self.f_2
        self.file_name_csv = self.mixed_f + '.csv'
        self.file_name_json = self.mixed_f + '.json'
        self.BASE_DIR = os.getcwd()
        self.dirname = 'observatory'
        self.check = ['REVIZE01']
        self.dict_box = []
        self.collector = []
        self.collector_REVIZE = []
        self.counter_ilksel = []
        self.counter_numline = []
        self.counter_REVIZE = []
        self.collect_thrd = []
        self._error = True
        self.cols = ['Tarih', 'Saat', 'Enlem(N)',
                     'Boylam(E)', 'Derinlik(km)',
                     'MD', 'ML', 'Mw', 'Yer',
                     'Çözüm-Niteliği']

        self.check_file = os.path.exists
        # specify the URL of the archive here ***
        self.archive_url = "http://www.koeri.boun.edu.tr/scripts/lst2.asp"
        #***



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
            #or
            # self.soup = BeautifulSoup(self.r.content, 'html.parser')

            # find all links on web-page
            self.text = self.soup.get_text()
            self.pre = self.soup.find_all('pre')[-1]
            self.get_text = self.pre.text

            for num_getText, i in enumerate(self.get_text.splitlines()[6:]):
                # print(num_getText, i)
                self.get_data += i + '\n'

            # print("end of lines: ",self.get_data.splitlines()[-1:])
            self.get_data = self.get_data[:-1]

            for num_line, line in enumerate(self.get_data.splitlines()):
                self.counter_numline.append(num_line)
                for num_partline, part_line in enumerate(line.split()):
                    if part_line == line.split()[0]:
                        self.dict = {}
                        for dict_index in range(len(self.cols[:7])):
                            self.dict[self.cols[dict_index]] = line.split()[dict_index]
                        self.collect = ''
                        self.collect_scnd = ''

                        # search for = Yer before last column
                    elif part_line not in self.check and part_line.isupper():
                        self.collect += part_line

                        # search for = 'REVİZE++' last column
                    elif part_line in self.check:
                        self.counter_REVIZE.append(part_line)
                        self.parse_REVIZE = ''
                        self.collect_scnd =line.split()[num_partline:][0:]
                        for z in self.collect_scnd:
                            self.parse_REVIZE += z + '-'
                            self.collect_scnd = self.parse_REVIZE[:-1]
                        self.collector_REVIZE.append(num_line)
                        # search for = 'İlksel' last column
                    elif part_line == line.split()[-1]:
                        for count_num in self.counter_numline:
                            if count_num in self.collector_REVIZE:
                                self.counter_numline.remove(count_num)

                self.dict[self.cols[8]] = self.collect
                self.dict[self.cols[9]] = self.collect_scnd
                self.dict_box.append(self.dict)

            for only_ilksel in self.counter_numline:
                self.last_part = self.get_data.splitlines()[only_ilksel].split()[-1]
                self.dict_box[only_ilksel][self.cols[9]] = self.last_part

        except (Exception) as error:
            print(error)
            self._error = False
            return -1
        finally:
            if self._error:
                if self.dict_box:
                    return self.dict_box

        #         # +++++++Check your data+++++++
        #         for num, i in enumerate(self.dict_box):
        #             print(num, i)
                pass


class GetDataJSON(GetBase):
    def __init__(self):
        super(GetDataJSON, self).__init__()
        self.data = GetLink().get_txt_links()
        # print(self.data)

    def create(self):
        try:
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
