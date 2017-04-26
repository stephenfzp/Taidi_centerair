# -*- coding: utf-8 -*-
# @Time    : 2017/3/14 9:32
# @Author  : stephenfeng
# @Software: PyCharm Community Edition

'''
读取数据并拆分
'''

import pandas as pd


data = pd.read_csv('G:\Python_Project\TaiDiBei\B\Data\data_2_change3.csv')

# # 添加一列‘外部温度差’
# data['temperture_minus'] = data['drybulb'] - data['wetbulb']
# data['cwshdr-cwrhdr'] = data['cwrhdr'] - data['cwshdr']

def divide_work_week(data, month, day_weekend):
    '把指定月的工作日和周末拆分出来'
    data = data[data['Month'] == int(month)]

    # 工作日的日期
    day_work = range(data['Day'].values[0], data['Day'].values[-1] + 1)
    for i in day_weekend:
        if i in day_work:
            day_work.pop(day_work.index(i))

    # 周末的数据   data_weekend
    data_weekend = pd.DataFrame(columns=data.columns)
    for i in day_weekend:
        data_weekend = pd.concat((data_weekend.iloc[:, :], data[data['Day'] == i].iloc[:, :]))

    # 工作日的数据  data_work
    data_work = data.drop(data_weekend.index)
    return data_work, data_weekend

#调用divide_work_week()函数把指定月份的数据拆分成工作日和周末
pre_data = data
data_10_work, data_10_week = divide_work_week(pre_data, 10, [8,9,15,16,22,23])
data_11_work, data_11_week = divide_work_week(pre_data, 11, [5,6,12,13,19,20,26,27])
data_12_work, data_12_week = divide_work_week(pre_data, 12, [3,4,10,11,17,18,24,25,31,26,27,28,29])

# #所有工作日和周末日
data_work = pd.concat((data_10_work, data_11_work, data_12_work))
data_weekend = pd.concat((data_10_week, data_11_week, data_12_week))

#   TODO:一天的时间划分为0-6、6-8、8-19、19-24

#工作日 拆分为4个时间段
data_work_on_1 = pd.concat((data_10_work[(data_10_work.Hour >= 0) & (data_10_work.Hour < 6) ], \
                            data_11_work[(data_11_work.Hour >= 0) & (data_11_work.Hour < 6)], \
                            data_12_work[(data_12_work.Hour >= 0) & (data_12_work.Hour < 6)]))

data_work_on_2 = pd.concat((data_10_work[(data_10_work.Hour >= 6) & (data_10_work.Hour < 8) ], \
                            data_11_work[(data_11_work.Hour >= 6) & (data_11_work.Hour < 8)], \
                            data_12_work[(data_12_work.Hour >= 6) & (data_12_work.Hour < 8)]))

data_work_on_3 = pd.concat((data_10_work[(data_10_work.Hour >= 8) & (data_10_work.Hour < 19) ], \
                          data_11_work[(data_11_work.Hour >= 8) & (data_11_work.Hour < 19)], \
                          data_12_work[(data_12_work.Hour >= 8) & (data_12_work.Hour < 19)]))

data_work_on_4 = pd.concat((data_10_work[(data_10_work.Hour >= 19) & (data_10_work.Hour < 24) ], \
                          data_11_work[(data_11_work.Hour >= 19) & (data_11_work.Hour < 24)], \
                          data_12_work[(data_12_work.Hour >= 19) & (data_12_work.Hour < 24)]))


#周末 拆分为4个时间段
data_weekend_1 = pd.concat((data_10_week[(data_10_week.Hour >= 0) & (data_10_week.Hour < 6) ], \
                             data_11_week[(data_11_week.Hour >= 0) & (data_11_week.Hour < 6)], \
                             data_12_week[(data_12_week.Hour >= 0) & (data_12_week.Hour < 6)]))

data_weekend_2 = pd.concat((data_10_week[(data_10_week.Hour >= 6) & (data_10_week.Hour < 8) ], \
                             data_11_week[(data_11_week.Hour >= 6) & (data_11_week.Hour < 8)], \
                             data_12_week[(data_12_week.Hour >= 6) & (data_12_week.Hour < 8)]))

data_weekend_3 = pd.concat((data_10_week[(data_10_week.Hour >= 8) & (data_10_week.Hour < 19) ], \
                             data_11_week[(data_11_week.Hour >= 8) & (data_11_week.Hour < 19)], \
                             data_12_week[(data_12_week.Hour >= 8) & (data_12_week.Hour < 19)]))

data_weekend_4 = pd.concat((data_10_week[(data_10_week.Hour >= 19) & (data_10_week.Hour < 24) ], \
                             data_11_week[(data_11_week.Hour >= 19) & (data_11_week.Hour < 24)], \
                             data_12_week[(data_12_week.Hour >= 19) & (data_12_week.Hour < 24)]))


#   TODO:有必要画图可视化下拟合的曲线和实际的值对比
