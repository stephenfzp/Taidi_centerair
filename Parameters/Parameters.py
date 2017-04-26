# -*- coding: utf-8 -*-
# @Time    : 2017/4/11 14:46
# @Author  : stephenfeng
# @Software: PyCharm Community Edition

#外部温度参数   （相对湿度、干球温度、湿球温度）
temper_parameters = ['rh','drybulb','wetbulb']


#设备控制参数   （冷水泵转速、冷凝水泵转速、冷却塔风扇转速）
service_parameters = ['chwp_pc', 'cwp_pc', 'ct_pc']


#状态参数
state_parameters = ['ch1stat','ch2stat','ch3stat','chwp1stat','chwp2stat','chwp3stat','chwp4stat',\
                    'cwp1stat','cwp2stat','cwp3stat', 'ct1stat','ct2stat']


#因变量    （总耗电量、冷却负载、系统效率、系统热平衡）
count_variable = ['systotpower', 'loadsys', 'effsys','hbsys']


#时间    （时间戳、年、月、日、时、分）
time = ['Time Stamp','Year','Month','Day','Hour','Minute']

#各个单独机器的功率
kw = ['ch1kw', 'ch2kw', 'ch3kw', 'chwp1kw', 'chwp2kw', 'chwp3kw', 'chwp4kw', \
      'cwp1kw', 'cwp2kw', 'cwp3kw', 'ct1kw', 'ct2kw']