# -*- coding: utf-8 -*-
# @Time    : 2017/3/19 14:15
# @Author  : stephenfeng
# @Software: PyCharm Community Edition

'''
预处理时的一些代码
'''

import pandas as pd
import numpy as np

###################  1  ###############
data = pd.read_csv('./data/data_2.csv')

# 总耗电量、冷却负载、系统效率、系统热平衡  把这几项移到数据集后面
count_variable = ['systotpower', 'loadsys', 'effsys','hbsys']
count = data[count_variable]
data.drop(count_variable, axis=1, inplace=True)
data[count_variable] = count
data.to_csv('./data/data_2_change.csv', index=False)

##################  2  ################
# 使用随机森林评估特征重要性
def random_forest_classifier(train_x, train_y):
    '随机森林分类器'
    from sklearn.ensemble import RandomForestRegressor
    model = RandomForestRegressor()
    model.fit(train_x, train_y)
    return model

count_variable = ['systotpower', 'loadsys', 'effsys','hbsys']
count = data_work[count_variable]
data_work.drop(count_variable, axis=1, inplace=True)
data_work.drop(['Time Stamp','Year','Month','Day','Hour','Minute'], axis=1, inplace=True)   #删除时间

randomForest_model = random_forest_classifier(data_work, count[count_variable[3]])    #randomForest_model.feature_importances_  #越高说明特征越重要
sort_feature_importances = sorted(zip(map(lambda x: round(x, 3), randomForest_model.feature_importances_), data_work.columns), reverse=True)
import pprint
pprint.pprint(sort_feature_importances)


#################  3  #########################
# 正则匹配时间序列 按照年、月、日、小时、分钟在原有数据中新增5列特征
import pandas as pd
import time
data = pd.read_csv('./data/data_2_change.csv')

pat = '(.+)/(.+)/(.{4}) (.+):(.+)'   #匹配出年月日
date = data['Time Stamp'].str.findall(pat)
#print date  #输出一个Series 包含匹配好的时间序列 eg:[(10, 4, 2016)]

data['Year'], data['Month'], data['Day'], data['Hour'], data['Minute'] = 0, 0, 0, 0, 0
start_time = time.time()
for i in range(data.shape[0]):
    data.loc[i, 'Year'] = date.values[i][0][2]
    data.loc[i, 'Month'] = date.values[i][0][0]
    data.loc[i, 'Day'] = date.values[i][0][1]
    data.loc[i, 'Hour'] = date.values[i][0][3]
    data.loc[i, 'Minute'] = date.values[i][0][4]
    print data.loc[i, ['Year', 'Month', 'Day', 'Hour', 'Minute']]
#print data.head().loc[:, ['Year', 'Month', 'Day', 'Hour', 'Minute']]
print '耗时:', str(time.time()-start_time)
print data.shape
data.to_csv('./data/data_2_change2.csv', index=False, encoding='utf-8', chunksize=10000)



def choose_feature_pearson(data, featurename, min):
    '筛选出和指定特征相关性满足min的数据   min：最小方差值'
    corrmat = data.corr()  # corr()：计算列与列的成对相关性，不包括NA /空值
    k = len(data.columns)
    cols = corrmat.nlargest(k, featurename)[featurename]
    cols = cols[cols > min].index
    return data[cols]

def rank_largest_pearson(data, featurename, k):
    '列出和指定特征皮尔孙相关性最大的前k个特征'
    corrmat = data.corr()
    cols = corrmat.nlargest(k, featurename)[featurename]
    return cols

def choose_feature_skew(data, min):
    '筛选出正偏斜度>min的特征 返回特征名'
    from scipy.stats import skew
    skewed_feats = data_work_8to19.apply(lambda x: skew(x.dropna()))  # 计算每个特征的偏斜度
    skewed_feats = skewed_feats[skewed_feats > min]  #筛选出偏斜度>min的特征
    return skewed_feats.index
skewed_feats = choose_feature_skew(data_work_8to19, 10)
data_work_8to19[skewed_feats] = np.log1p(data_work_8to19[skewed_feats])  #对筛选出的偏斜度大的特征进行对数转换



#############################   ########################
# 利用箱线图的原理剔除异常值
# 获取该数据的日期
def handle_exception(data, month, featurename):
    '剔除离群点'
    nowdata = data[data['Month'] == int(month)]
    day_list = sorted(list(nowdata['Day'].value_counts().index)) # 该月份的日期列表
    outlier_list = []  #放置离群点的索引值
    for day in day_list:
        nowdata2 = nowdata[nowdata['Day'] == day]
        hour_list = sorted(list(nowdata2['Hour'].value_counts().index)) #指定日期的当天时间列表
        for hour in hour_list:
            nowdata3 = nowdata2[nowdata2['Hour'] == hour]
            nowdata3_1 = nowdata3[nowdata3['Minute'] <= 30]  #每隔半小时
            nowdata3_2 = nowdata3[nowdata3['Minute'] > 30]

            one_describe = nowdata3_1[featurename].describe()
            two_describe = nowdata3_2[featurename].describe()

            LowerLimit_one = 2.5 * one_describe.ix['25%'] - 1.5 * one_describe.ix['75%']
            UpperLimit_one = 2.5 * one_describe.ix['75%'] - 1.5 * one_describe.ix['25%']
            LowerLimit_two = 2.5 * two_describe.ix['25%'] - 1.5 * two_describe.ix['75%']
            UpperLimit_two = 2.5 * two_describe.ix['75%'] - 1.5 * two_describe.ix['25%']

            list1 = nowdata3_1[ (nowdata3_1[featurename] < LowerLimit_one) | (nowdata3_1[featurename] > UpperLimit_one) ].index.values
            list2 = nowdata3_2[ (nowdata3_2[featurename] < LowerLimit_two) | (nowdata3_2[featurename] > UpperLimit_two) ].index.values

            outlier_list += list(list1)
            outlier_list += list(list2)
    print len(outlier_list)
    nowdata.drop(outlier_list, axis=0, inplace=True)
    return nowdata

data_10 = handle_exception(data, 10, 'systotpower')  # 10月份删除了745个离群点
data_11 = handle_exception(data, 11, 'systotpower')  # 11月份删除了686个离群点
data_12 = handle_exception(data, 12, 'systotpower')  # 12月份删除了893个离群点

print data.shape
data = pd.concat((data_10, data_11, data_12))  # 原始数据量为88840行， 去除异常点后剩下86516行数据
#data.to_csv('./data/data_2_change3.csv', index=False)
print data.shape