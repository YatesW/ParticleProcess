#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import numpy as np
import os
import warnings

warnings.filterwarnings('ignore')



class IterMethod:

    def __init__(self, data_df, metric_df):
        '''
        data_csv: 清洗后的df
        metric_csv: 清洗后数据统计指标的df
        '''
        self.data_df = data_df
        self.metric_df = metric_df
        self.col_name = self.data_df.columns.tolist()

        self.cur_df = self.data_df  # 每次要进行被迭代的df

        self.iter_cnt = 0  # 迭代次数
        self.all_thr = list()  # 每次迭代后得到的阈值

    def get_avg(self):
        '''
        求出每种粒子强度的平均值，返回nparray
        '''
        return np.nanmean(self.cur_df, axis=0)

    def get_std(self):
        '''
        求出每种粒子强度的标准差，返回nparray
        '''
        return np.nanstd(self.cur_df, axis=0)

    def get_thr(self):
        '''
        求出每个csv文件的阈值,并更新self.iter_cnt, self.all_thr
        '''
        avg_tmp = self.get_avg()
        std_tmp = self.get_std()
        thr = np.nanmean(3 * std_tmp + avg_tmp)
        self.all_thr.append(thr)
        self.iter_cnt += 1
        return thr

    def gt_file(self, cnt):
        '''
        创建gt文件夹并返回对应迭代轮数的csv文件名
        '''
        dir_path = os.path.join(os.getcwd(), "gt")
        flag = os.path.exists(dir_path)
        if not flag:
            os.makedirs(dir_path)
        file_name = str(cnt) + ".csv"
        file_path = os.path.join(dir_path, file_name)
        return file_path

    def lt_file(self, cnt):
        '''
        创建lt文件夹并返回对应迭代轮数的csv文件名, 如：gt/1.csv
        '''
        dir_path = os.path.join(os.getcwd(), "lt")
        flag = os.path.exists(dir_path)
        if not flag:
            os.makedirs(dir_path)
        file_name = str(cnt) + ".csv"
        file_path = os.path.join(dir_path, file_name)
        return file_path

    def update_df(self, thr, cnt):
        '''
        根据阈值保存为两个csv文件：'gt/1.csv'、'lt/1.csv'；并返回小于阈值的df
        '''
        gt_df = self.cur_df[self.cur_df >= thr]
        gt_df.to_csv(self.gt_file(cnt), index=None)
        lt_df = self.cur_df[self.cur_df < thr]
        lt_df.to_csv(self.lt_file(cnt), index=None)
        print("The %s th iteration have been finished." % cnt)
        return lt_df

    def iterator(self):
        '''
        迭代过程
        '''
        beg_DF = self.cur_df
        end_DF = self.cur_df
        flag = False
        while not flag:
            beg_DF = end_DF
            THR = self.get_thr()  # self.iter_cnt 在此处已+1
            end_DF = self.update_df(THR, self.iter_cnt)
            self.cur_df = end_DF
            if beg_DF.equals(end_DF):
                flag = True

    def get_final_result(self, resolve_data):
        '''
        输入：溶解态的最终结果为 lt/last_iter_cnt.csv
        结果：得到颗粒态的最终结果 gt/last_iter_cnt+1.csv
        '''
        resolve_df = pd.read_csv(resolve_data)
        particle_df = self.data_df[pd.isnull(resolve_df)]
        # pd.isnull(resolve_df_：溶解态df的非空位为False，空位为True，与清洗后的原始数据做mask
        particle_df.to_csv(self.gt_file(self.iter_cnt + 1), index=None)


