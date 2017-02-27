# !/bin/env python
# coding = utf-8

import re
from datetime import datetime
import sys
from base_tool import *
import codecs

FILE_PATH = 'D:\\Work\\性能\\交行cac\\result\\antivi_1000\\da_anti1000.log'

# creat anction cost_list & return time : avg cost`
# T:2771883776(14:59:05)[S:EC69][root:Debug] AQAAfwD3_zO5Sk5YiAQAAA--.4W write tmp file:/home/coremail/var/antivirus/
da_anti_start_re = \
    re.compile(r'T:\d+.*\((\d+:\d+:\d+)\).*\s(\S+--\.[\d|\w]+) write tmp file:/home/coremail/var/antivirus')
# AQAAfwD3_zO5Sk5YiAQAAA--.4W scan result:0(No Virus),Engine:Sophos engine
da_anti_end_re = re.compile(r'T:\d+.*\((\d+:\d+:\d+)\).*\s(\S+--\.[\d|\w]+) scan result:.*Engine:')
# Part Scan Result:3(Virus is not killed), scan only:0, costs 84 ms,Engine:Sophos Antivirus engine
anti_time = re.compile(r'T:\d+.*\((\d+:\d+:\d+)\).*Scan Result.*costs (\d+) ms')

da_has_data = False
anti_has_data = False
# da_anti_cost_list = {}   # da_anti_cost_list['time'] = time_cost_all
tid_start_time_list = {}
tid_end_time_list = {}
da_anti_count_list = {}  # da_anti_count_list['time'] = success_count
anti_cost_list = {}  # anti_cost_list{'time'} = time_coat_all
anti_count_list = {}  # anti_count_list{'time'} = success_count
# FILE_PATH = '360cost09031430.txt'

da = codecs.open(FILE_PATH, 'r')
for line in da:
    da_anti_start = da_anti_start_re.search(line)
    da_anti_end = da_anti_end_re.search(line)
    anti_cost = anti_time.search(line)
    if da_anti_start is not None:
        tmp = da_anti_start.groups()
        if tmp[1] not in tid_start_time_list.keys():
            time = datetime.strptime(tmp[0], '%H:%M:%S')
            tid_start_time_list[tmp[1]] = time  # tid_start_time_list['tid'] = time

    if da_anti_end is not None:
        tmp = da_anti_end.groups()
        time = datetime.strptime(tmp[0], '%H:%M:%S')
        if time not in da_anti_count_list.keys():
            da_anti_count_list[time] = 0
        da_anti_count_list[time] += 1     ### creat da_anti_count_list['time'] = success_count
        if tmp[1] in tid_start_time_list.keys():  # tid must be in start_list
            tid_end_time_list[tmp[1]] = time  # tid_end_time_list['tid'] = end_time
        da_has_data = True

    if anti_cost is not None:
        tmp = anti_cost.groups()
        time = datetime.strptime(tmp[0], '%H:%M:%S')
        if time not in anti_cost_list.keys():
            anti_cost_list[time] = 0
            anti_count_list[time] = 0
        anti_cost_list[time] += int(tmp[1])     # creat anti_cost_list
        anti_count_list[time] += 1  ### creat anti_count_list
        anti_has_data = True
# if da_has_data:
da_anti_cost_list = action_cost_avg(da_anti_count_list, start_time_list=tid_start_time_list, end_time_list=tid_end_time_list)
# if anti_has_data:
anti_cost_list = action_cost_avg(anti_count_list, anti_cost_list)


if __name__ == '__main__':
    if da_anti_cost_list:
        title = 'daliveragent antivirus cost time(s)/avg'
        y_text = 'avg time(s)'
        draw_and_save(title, y_text, da_anti_cost_list, FILE_PATH, 'da_anti_cost')

    if da_anti_count_list:
        title = 'daliveragent antivirus success /s'
        y_text = 'success/s'
        draw_and_save(title, y_text, da_anti_count_list, FILE_PATH, 'da_anti_count')

    if anti_cost_list:
        title = 'antivirus cost time(ms)/avg'
        y_text = 'avg time(ms)'
        draw_and_save(title, y_text, anti_cost_list, FILE_PATH, 'anti_cost')

    if anti_count_list:
        title = 'antivirus success /s'
        y_text = 'success/s'
        draw_and_save(title, y_text, anti_count_list, FILE_PATH, 'anti_count')
