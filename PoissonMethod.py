#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import numpy as np
import warnings

warnings.filterwarnings('ignore')



class PoissonMethod:

    def __init__(self, data_df, metric_df, credible):
        '''
        data_df：清洗后数据的df
        metric_df：清洗后数据统计指标的df
        credible：置信度。小数表示，如0.997
        '''
        self.data_df = data_df
        self.metric_df = metric_df
        self.col_name = self.data_df.columns.tolist()
        self.m = self.metric_df.iloc[5]  # 未归一化的强度均值，归一化处理后作为λ
        self.credible = credible


    def normal_lambda(self):
        '''
        将强度均值归一化，得到可用于泊松计算λ。
        返回的df包括每种粒子的 [强度均值，λ，scale], 并保存该df，每行都是float。
        '''
        lamb_li = []  # 每种粒子归一化后的λ
        scale_li = []  # 每种粒子的缩放系数scale
        scale = 1.0
        for val in self.m:
            if val > 0 and val <= 1:
                scale = 50.0
            elif val > 1 and val <= 2:
                scale = 25.0
            elif val > 2 and val <= 3:
                scale = 15.0
            elif val > 3 and val <= 35:
                scale = 1.0
            else:
                scale = 0.33
            lamb_li.append(round(val * scale))
            scale_li.append(scale)

        lamb_li = np.array(lamb_li).reshape(1, -1)
        scale_li = np.array(scale_li).reshape(1, -1)
        res_arr = np.concatenate((lamb_li, scale_li), axis=0)
        res_df = pd.DataFrame(res_arr, columns=self.col_name)
        res_df = pd.concat([self.m.to_frame().T, res_df])
        res_df.insert(0, 'metric', value=['avg_ints', 'lambda', 'scale'])
        res_df.set_index(['metric'], inplace=True)  # metric 列作为index
        file_name = "poisson_normalize_lambda.csv"
        res_df.to_csv(file_name)
        return res_df


    def poisson(self, k, lamb):
        '''
        泊松方程，计算得到单词的概率值。在计算最终阈值时需要将概率累加
        lamb：归一化后的λ,一定是整数
        '''
        kjie = 1  # k!
        for i in range(1, k):
            kjie *= i
        lamb = float(lamb)
        pk = np.power(lamb, k) / kjie * np.exp(-lamb)
        return pk


    def get_ints_thr(self):
        '''
        计算得到每种元素的阈值df，并保存
        '''
        lamb = self.normal_lambda().iloc[1].values.astype('int')
        scale = self.normal_lambda().iloc[2].values
        ints_val = []
        for i in range(len(self.col_name)):
            thr = 0.0
            prob = 0.0
            for k in range(1, 100):
                prob += self.poisson(k, lamb[i])
                if prob >= self.credible:
                    thr = k / scale[i]
                    break
            ints_val.append(thr)
        ints_val = pd.DataFrame(np.array(ints_val).reshape(1, -1), columns=self.col_name)
        file_name = "intensity_threshold.csv"
        ints_val.to_csv(file_name, index=None)
        return ints_val


    def classifier(self):
        '''
        根据每种元素强度的阈值区分颗粒态和溶解态粒子，分别保存为df
        '''
        resolve = pd.DataFrame()  # 分类后的溶解态粒子数据
        particle = pd.DataFrame()  # 分类后的颗粒态粒子数据
        ints_thr = self.get_ints_thr()
        ints_thr_li = ints_thr.values[0]

        for idx in range(len(self.col_name)):
            single_ptc_df = self.data_df.iloc[:, idx].to_frame()
            single_ptc_resolve = single_ptc_df[single_ptc_df >= ints_thr_li[idx]]
            particle = pd.concat([particle, single_ptc_resolve], axis=1)

        resolve = self.data_df[pd.isnull(particle)]
        particle.to_csv("Poisson_particle.csv", index=None)
        print("Particle have been saved.")
        resolve.to_csv("Poisson_resolve.csv", index=None)
        print("Resolve have been saved.")


