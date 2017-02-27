#!/bin/evn python
# coding = utf-8

import re
from datetime import datetime
import codecs
import sys

FILE_PATH = sys.argv[1]


def action_cost_avg(count_list, all_cost_list=None, start_time_list=None, end_time_list=None):
    cost_list = {}
    if all_cost_list is None:
        for tid in end_time_list.keys():
            # if tid in tid_start_time_list.keys():  # tid must be in tid_start_time_list
            if end_time_list[tid] not in cost_list.keys():
                cost_list[end_time_list[tid]] = 0
            y = end_time_list[tid]
            x = start_time_list[tid]
            cost_list[end_time_list[tid]] = + int((y - x).seconds)  # .seconds: by seconds
    else:
        cost_list = all_cost_list
    for action_time in count_list.keys():
        if action_time in cost_list.keys():
            cost_list[action_time] = float(cost_list[action_time] / count_list[action_time])
    return cost_list


def get_point(time_y_plot):
    sort_point_map = sorted(time_y_plot.items(), key=lambda d: d[1])
    # get 90% point
    d_len = int(len(sort_point_map)*0.9)
    a = sort_point_map[d_len][0].strftime('%H:%M:%S')  # time
    b = sort_point_map[d_len][1]  # point
    return [a, b]

# Successfully put mail to ms 1 , msgid:1tbiAQANBFdEe9oAAQAIsz
tid_start_re = re.compile(r'T:(\d+)\((\d+:\d+:\d+).*Try to apply CACID.*for checkMailByCAC')
#  AQAAfxAHilUJgEpYRAoAAA--.6W  get CACCheck result from CAC
tid_end_re = re.compile(r'T:(\d+)\((\d+:\d+:\d+).*get CACCheck result from CAC')

tid_start_list = {}
tid_end_list = {}
cac_cost_list = {}
cac_count_list = {}

cac = codecs.open(FILE_PATH, 'r', 'utf-8')
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
        a = get_point(cac_cost_list)
        print(title+'/90 per: time: %s y: %.2f ' % (a[0], a[1])+y_text)

    if cac_count_list:
        title = 'deliveragent CAC success/s'
        y_text = 'success/s'
        a = get_point(cac_count_list)
        print(title+'/90 per: time: %s y: %.2f ' % (a[0], a[1])+y_text)
