#!/bin/evn python
# coding = utf-8

import re
from base_tool import *
from datetime import datetime
import codecs
import sys

FILE_PATH = 'D:\\Work\\性能\\交行cac\\result\\cac_5000\\da_cac5000.log'
# Successfully put mail to ms 1 , msgid:1tbiAQANBFdEe9oAAQAIsz
tid_start_re = re.compile(r'T:(\d+)\((\d+:\d+:\d+).*Try to apply CACID.*for checkMailByCAC')
#  AQAAfxAHilUJgEpYRAoAAA--.6W  get CACCheck result from CAC
tid_end_re = re.compile(r'T:(\d+)\((\d+:\d+:\d+).*get CACCheck result')

tid_start_list = {}
tid_end_list = {}
cac_cost_list = {}
cac_count_list = {}
success_count = 0
cac = codecs.open(FILE_PATH, 'r')
for cac_line in cac:
    tid_start = tid_start_re.search(cac_line)
    tid_end = tid_end_re.search(cac_line)
    if tid_start is not None:
        tid_tmp = tid_start.groups()
        cac_time = datetime.strptime(tid_tmp[1], '%H:%M:%S')
        tid_start_list[tid_tmp[0]] = cac_time  # tid_start_list['tid'] = time
    if tid_end is not None:
        tid_tmp = tid_end.groups()
        cac_time = datetime.strptime(tid_tmp[1], '%H:%M:%S')
        if cac_time not in cac_count_list.keys():  # creat cac_count_list['time'] = count
            cac_count_list[cac_time] = 0
        cac_count_list[cac_time] += 1
        success_count += 1
        if tid_tmp[0] in tid_start_list.keys():
            if cac_time not in cac_cost_list.keys():
                cac_cost_list[cac_time] = 0  # creat cac_cost_list['time'] = all time
            cac_cost_list[cac_time] += int((cac_time - tid_start_list[tid_tmp[0]]).seconds)
            tid_start_list.pop(tid_tmp[0])

cac_cost_list = action_cost_avg(cac_count_list, cac_cost_list)

if __name__ == '__main__':
    if cac_cost_list:
        title = 'deliveragent CAC cost time(s)/avg'
        y_text = 'avg time(s)'
        # draw_and_save(title, y_text, cac_cost_list, FILE_PATH, 'cac_cost')
        print("cac_cost_list: %d" % success_count)

    if cac_count_list:
        title = 'deliveragent CAC success/s'
        y_text = 'success/s'
        # draw_and_save(title, y_text, cac_count_list, FILE_PATH, 'cac_count')
        print("cac_count_list: %d" % success_count)
