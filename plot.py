# -*- coding: utf-8 -*-
# @Time    : 2017/3/18 18:54
# @Author  : stephenfeng
# @Software: PyCharm Community Edition

'''
画图可视化
'''

import pandas as pd
import numpy as np
import seaborn as sns
from pylab import *
mpl.rcParams['font.sans-serif'] = ['SimHei']   #AR PL UMing CN代表：宋体。SimHei代表：黑体
mpl.rcParams['axes.unicode_minus'] = False  #解决负号问题
import sys
reload(sys)
sys.setdefaultencoding('utf8')


def plot_heatmap(data, featurename, k):
    '绘制数据中指定某个特征的相关热图   featurename：特征名   k：相关度由大到小排序前k个'
    import seaborn as sns
    import matplotlib.pyplot as plt
    corrmat = data.corr()   #corr()：计算列与列的成对相关性，不包括NA /空值
    cols = corrmat.nlargest(k, featurename)[featurename].index
    labels = list(cols.values) #x轴和y轴的标签
    cm = np.corrcoef(data[cols].values.T)
    print corrmat.nlargest(k, featurename)[featurename]   #生成一个series
    sns.set(font_scale=1.25)
    ax = sns.heatmap(cm, cbar=True, annot=True, square=True, fmt='.2f', annot_kws={'size': 15})
    ax.set_xticklabels(labels, rotation=45)
    labels.reverse()
    ax.set_yticklabels(labels, rotation='horizontal')
    plt.title(cols[0])
    sns.plt.show()
plot_heatmap(data_work, count_variable[0],20)


# 预测结果和真实结果绘图对比
data = pd.concat((y_train, data_work_8to19_time), axis=1)
data['predict'] = all_pre

y_label = 'systotpower'
start, end =5,6
m,n = 1,end-start+1
fig = plt.figure()
for i in range(1, end-start+2):
    ax1 = fig.add_subplot(m, n, i)

    count = data[data['Day'] == start]  #指定天数的所有数据
    label = str(start)+'号'
    start += 1

    xticks = range(0, count.shape[0], 20)
    xlabel = [count['Hour'].reset_index(drop=True)[i] for i in xticks]

    ax1.set_xticks(xticks)
    ax1.set_xticklabels(xlabel, rotation=90)

    ax1.scatter(range(count.shape[0]), count[y_label], s=3)  #, label=label, marker='*'
    ax1.plot(range(count.shape[0]), count['predict'], color='b')

    ax1.set_title(label)
    plt.xlim(xmin=0); plt.ylim(0)
    plt.grid()  #显示网格

plt.subplots_adjust(wspace=0)
plt.suptitle('横坐标：时间  纵坐标：系统效率', fontsize=25)
# plt.savefig('test.png', dpi = 1000)
plt.show()


def plot_box(data, featurename, daymonth, daynum):
    '传入数据、指定的列名和指定的月日，绘制箱线图'
    count = data[ (data['Month'] == int(daymonth)) & (data['Day'] == int(daynum))]
    data = pd.concat([count['Hour'], count[featurename]], axis=1)
    import seaborn as sns
    ax = sns.boxplot(x=data.columns[0], y=data.columns[1], data=data)
    #ax = sns.stripplot(x=data.columns[0], y=data.columns[1], data=data, jitter=True, edgecolor="gray")
    plt.grid()  # 显示网格
    #sns.plt.savefig('a.png', dpi = 250)
    sns.plt.show()
plot_box(data_work_on_1, 'systotpower', 12, 21)


def plot_box(data, featurename, daymonth):
    '绘制箱线图 并自动保存到本地指定文件夹里面'
    data = data[data['Month'] == int(daymonth)]  #当前月的数据
    day_list = sorted(list(data['Day'].value_counts().index))  #日期列表 1-30
    print day_list
    for i in day_list:
        now_data = data[data['Day'] == i]
        #hour_list = sorted(list(now_data['Hour'].value_counts().index))
        now_data = pd.concat([now_data['Hour'], now_data[featurename]], axis=1)
        ax = sns.boxplot(x=now_data.columns[0], y=now_data.columns[1], data=now_data)

        plt.grid()  # 显示网格
        sns.plt.title(str(daymonth)+u'月——'+str(i)+u'号')
        sns.plt.savefig('./Boxplots/'+str(daymonth)+u'月——'+str(i)+u'号'+'.png', dpi = 250)
        sns.plt.clf()
        #sns.plt.show()
plot_box(data_work_on_1, 'systotpower', 11)


def distributed_diagram(data, featurename):
    '根据指定的特征绘制分布图'
    # import seaborn as sns
    # fig = plt.figure()
    # ax = fig.add_subplot(111)
    plt.hist(data[featurename])
    plt.title(featurename)
    plt.show()
distributed_diagram(data, 'dch')


def plot_two_feature(data, x_label, y_label):
    '绘制指定两个变量的二维图像'
    fig = plt.figure();ax1 = fig.add_subplot(111)
    ax1.scatter(data[x_label], data[y_label], s=3, color='blue')  # marker='*'
    #ax1.scatter(data[x_label], data['chwrhdr'], s=3, color='red')
    ax1.set_xlabel(x_label);ax1.set_ylabel(y_label)
    ax1.set_title('横坐标：'+ x_label+ ' 纵坐标：'+y_label, fontsize=25)

    plt.grid()  # 显示网格
    plt.xlim(xmin=0);plt.ylim(0)
    plt.show()
plot_two_feature(train_data, 'loadsys / cwp_P', 'cwrhdr')


def heat(data, featurename, k):
    '输出其他特征和指定特征的相关系数 输出一个Series'
    corrmat = data.corr()   #corr()：计算列与列的成对相关性，不包括NA /空值
    print corrmat.nlargest(k, featurename)[featurename]   #生成一个series
heat(train_data, 'cwp_P', 30)


def plot_every_month_distributed(data, month, label_name):
    '输出指定月份的每天分布图'
    m, n = 5, 6
    data = data[data['Month'] == int(month)]
    day_list = sorted(list(data['Day'].value_counts().index))
    print day_list
    fig = plt.figure()
    for i in range(0, m * n):
        if i <= len(day_list) - 1:
            ax1 = fig.add_subplot(m, n, i + 1)
            count = data[data['Day'] == day_list[i]]  # 指定的天数
            label = str(day_list[i]) + '号'

            xticks = range(0, count.shape[0], 60)
            xlabel = [count['Hour'].reset_index(drop=True)[i] for i in xticks]
            ax1.set_xticks(xticks)
            ax1.set_xticklabels(xlabel, rotation=90)

            ax1.scatter(range(count.shape[0]), count[str(label_name)], s=3, color='blue')  # , label=label, marker='*'
            # ax1.scatter(range(count.shape[0]), count[y_label2], s=3, color='red')
            ax1.set_title(label)
            plt.grid()  # 显示网格
            plt.xlim(xmin=0, xmax=count.shape[0] + 1)
            plt.ylim(ymin=-1, ymax=1.5)

    plt.subplots_adjust(hspace=0.4)
    plt.suptitle(str(month) +'月——横坐标：时间  纵坐标：'+str(label_name), fontsize=25)
    plt.show()
plot_every_month_distributed(data, 12, 'chwp2stat')


# 单独生成指定时间的分布图
y_label = 'systotpower'
start, end = 3,3
m,n = 1,end-start+1
fig = plt.figure()
for i in range(1, end-start+2):
    ax1 = fig.add_subplot(m, n, i)

    count = data[data['Day'] == start]  #指定天数的所有数据
    label = str(start)+'号'
    start += 1

    xticks = range(0, count.shape[0], 10)
    xlabel = [count['Hour'].reset_index(drop=True)[i] for i in xticks]

    ax1.set_xticks(xticks)
    ax1.set_xticklabels(xlabel, rotation=90)

    ax1.scatter(range(count.shape[0]), count[y_label], s=3)  #, label=label, marker='*'
    ax1.scatter(range(count.shape[0]), count[y_label], s=3, color='b')

    ax1.set_title(str(data['Month'].values[0]) +'月 '+label)
    plt.xlim(xmin=0); plt.ylim(0)
    plt.grid()  #显示网格

plt.subplots_adjust(wspace=0)
plt.suptitle('横坐标：时间  纵坐标：总耗电量', fontsize=25)
# plt.savefig('test.png', dpi = 1000)
plt.show()