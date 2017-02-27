#!/bin/evn python
# coding = utf-8

import pylab as py
from matplotlib.dates import SecondLocator, DateFormatter


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


# time_y_plot={time:point} d_interval :s
def draw_plot(title, time_y_plot, lable_text, d_interval=120):
    x_p = []
    y_p = []
    sort_time_map = sorted(time_y_plot.items(), key=lambda d: d[0])
    sort_point_map = sorted(time_y_plot.items(), key=lambda d: d[1])
    # get 90% point
    d_len = int(len(sort_point_map)*0.9)
    a = sort_point_map[d_len][0]  # time
    b = sort_point_map[d_len][1]  # point
    for i in sort_time_map:
        x_p.append(i[0])
        y_p.append(i[1])

    ax = py.subplot(111)
    xmajorFormatter = DateFormatter('%H:%M:%S')  # set y text format
    ax.xaxis.set_major_formatter(xmajorFormatter)
    # ax.xaxis.set_major_locator(SecondLocator(interval=d_interval)
    py.plot(x_p, y_p, marker='o')
    py.text(a, b, '90%y={1:.2f}({0:%H:%M:%S})'.format(a, b), color='red', bbox=dict(facecolor='white', alpha=0.6))
    py.plot(a, b, 'or-')   # point 90%
    py.title(title)     # give plot a title
    py.xlabel('time')     # make axis labels
    py.ylabel(lable_text)
    py.grid(True)
    # py.show()
    return [sort_time_map, py]


def draw_and_save(s_title, s_y_text, save_list, path, name):
    sav_tmp = []
    int_date = draw_plot(s_title, save_list, s_y_text)
    tp = int_date[0]
    tp_point = int_date[1]
    for sav_change in tp:
        sav_tmp.append(sav_change[0].strftime('%H:%M:%S')+','+str(sav_change[1]))
    with open(path+'-'+name+'.dat', 'w') as sav:
        sav.write('\n'.join(sav_tmp))
    tp_point.savefig(path+'-'+name+'.png', format='png')
    tp_point.close()
