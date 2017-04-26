# -*- coding: utf-8 -*-
# @Time    : 2017/4/12 11:04
# @Author  : stephenfeng
# @Software: PyCharm Community Edition

'''
分析工作日的数据
'''
from Loaddata.load_data import *
from Parameters.Parameters import *

import pandas as pd
import numpy as np

import warnings
warnings.filterwarnings("ignore")

from sklearn.linear_model import RidgeCV, LassoCV, ElasticNetCV, SGDRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.neural_network import MLPRegressor
from sklearn import model_selection
from sklearn.metrics import mean_squared_error, r2_score



# TODO:一天的时间划分为0-6、6-8、8-19、19-24

####################### 1、耗电量 #################################
useful_variable = data_work_on_3.columns.difference(state_parameters)  #排除12个状态参数特征 + 时间特征
data = data_work_on_3[useful_variable]



# #标准化数据集  只需对原来不是状态参数的特征进行标准化
alldata = data
from sklearn import preprocessing
data_scale = preprocessing.scale(alldata.iloc[:,:-1], axis=0)
alldata.iloc[:,:-1] = data_scale

ntrain = alldata.shape[0]
x_train = alldata.iloc[:,:-1]; x_train = np.array(x_train) #转为numpy数组
y_train = alldata.iloc[:,-1]; y_train = np.array(y_train)

#设置KFold交叉验证
from sklearn.cross_validation import KFold
NFOLDS = 5
SEED = 0
kf = KFold(ntrain, n_folds=NFOLDS, shuffle=True, random_state=SEED)
def get_oof(model): #传入一个model
    oof_train = np.zeros((ntrain,))
    oof_test = np.zeros((ntrain,))
    oof_test_skf = np.empty((NFOLDS, ntrain))

    for i, (train_index, test_index) in enumerate(kf): #迭代次数为NFOLDS次
        x_tr = x_train[train_index]
        y_tr = y_train[train_index]
        x_te = x_train[test_index]

        model.fit(x_tr, y_tr)
        oof_train[test_index] = model.predict(x_te)
        oof_test_skf[i, :] = model.predict(x_train)  # 根据训练好的模型来测试全部测试集
    oof_test[:] = oof_test_skf.mean(axis=0)
    print 'model.score：', model.score(x_train, y_train)
    print 'model.coef_ & model.intercept_：', model.coef_, model.intercept_
    print 'r2_score:', r2_score(y_train, oof_train), r2_score(y_train, oof_test)
    return mean_squared_error(y_train, oof_train), mean_squared_error(y_train, oof_test)

ridgecv = RidgeCV(fit_intercept=True, cv=8)
lassocv = LassoCV(fit_intercept=True, cv=8, selection='random')
elasticcv = ElasticNetCV(fit_intercept=True, cv=8)
mlpregressor = MLPRegressor(hidden_layer_sizes=(10,5))
sgdclassifier = SGDRegressor(fit_intercept=True)
randomregressor = RandomForestRegressor()

print get_oof(ridgecv)
print get_oof(lassocv)
print get_oof(elasticcv)
print get_oof(sgdclassifier)
print get_oof(randomregressor)
print get_oof(mlpregressor)

















