# !/bin/env python
# coding = utf-8

import re
from datetime import datetime
import sys
import codecs
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

# creat anction cost_list & return time : avg cost
# T:2771883776(14:59:05)[S:EC69][root:Debug] AQAAfwD3_zO5Sk5YiAQAAA--.4W write tmp file:/home/coremail/var/antivirus/
da_anti_start_re = \
    re.compile(r'T:\d+.*\((\d+:\d+:\d+)\).*\s(\S+--\.[\d|\w]+) write tmp file:/home/coremail/var/antivirus')
# AQAAfwD3_zO5Sk5YiAQAAA--.4W scan result:0(No Virus),Engine:Sophos engine
da_anti_end_re = re.compile(r'T:\d+.*\((\d+:\d+:\d+)\).*\s(\S+--\.[\d|\w]+) scan result:.*Engine:')
# Part Scan Result:3(Virus is not killed), scan only:0, costs 84 ms,Engine:Sophos Antivirus engine
anti_time = re.compile(r'P:\d+.*\((\d+:\d+:\d+)\).*Scan Result.*costs (\d+) ms')

da_has_data = False
anti_has_data = False
# da_anti_cost_list = {}   # da_anti_cost_list['time'] = time_cost_all
tid_start_time_list = {}
tid_end_time_list = {}
da_anti_count_list = {}  # da_anti_count_list['time'] = success_count
anti_cost_list = {}  # anti_cost_list{'time'} = time_coat_all
anti_count_list = {}  # anti_count_list{'time'} = success_count
# FILE_PATH = '360cost09031430.txt'

da = codecs.open(FILE_PATH, 'r', 'utf-8')
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
        a = get_point(da_anti_cost_list)
        print(title+'/90 per: time: %s y: %.2f ' % (a[0], a[1])+y_text)

    if da_anti_count_list:
        title = 'daliveragent antivirus success /s'
        y_text = 'success/s'
        a = get_point(da_anti_count_list)
        print(title+'/90 per: time: %s y: %.2f ' % (a[0], a[1])+y_text)

    if anti_cost_list:
        title = 'antivirus cost time(ms)/avg'
        y_text = 'avg time(ms)'
        a = get_point(anti_cost_list)
        print(title+'/90 per: time: %s y: %.2f ' % (a[0], a[1])+y_text)

    if anti_count_list:
        title = 'antivirus success /s'
        y_text = 'success/s'
        a = get_point(anti_count_list)
        print(title+'/90 per: time: %s y: %.2f ' % (a[0], a[1])+y_text)
