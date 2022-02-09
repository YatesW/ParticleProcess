#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import numpy as np
import warnings

warnings.filterwarnings('ignore')



class DataLoader:
    
    def __init__(self, ori_file_name):   
        '''
        ori_file_name:原始数据文件的文件名。(原始数据放在当前目录下即可)
        '''
        self.ori_file_name = ori_file_name
        self.ori_df = pd.read_csv(ori_file_name).iloc[:,2:]   # 原始数据的df (去掉index和timestamp)
        self.col_name = self.ori_df.columns.tolist()   # 完整粒子名
        
        
    def get_ptc_name(self):  
        '''
        返回剥离多余符号后的粒子名，如：46Ti
        '''
        short_name = list(map(lambda x:x[1:-8], self.col_name))
        return short_name
    
    
    def get_cleaned_data(self):  
        '''
        清洗数据，将负值置为0, 并保存清洗后的数据
        '''
        cleaned_df = self.ori_df.copy()
        cleaned_df[cleaned_df<=0]=np.nan   # 不大于0的区域全部置为nan
        file_name = 'cleaned_'+ self.ori_file_name
        cleaned_df.to_csv(file_name, index=None)
        print('%s have been saved.' % file_name)
        return cleaned_df
    
    
    def get_basic_metirct(self, cleaned_df): 
        '''
        得到 [去除符号后的粒子名，每种粒子出现的次数,最小强度，最大强度，平均强度，总强度，强度标准差] 的df；
        并插入metirc列作为index；最后保存
        cleaned_df：get_cleaned_data得到的清洗后数据的df
        '''
        basic_metric = pd.DataFrame()
        short_name = pd.DataFrame(np.array(self.get_ptc_name()).reshape(1,-1), columns=self.col_name)   # 去除符号后的粒子名
        count = cleaned_df[cleaned_df>0].count().to_frame().T     # 某种粒子出现次数
        min_ints = cleaned_df.min().to_frame().T    # 某种粒子强度最小值
        max_ints = cleaned_df.max().to_frame().T    # 某种粒子强度最大值
        sum_ints = pd.DataFrame(np.nansum(cleaned_df, axis=0).reshape(1,-1), columns=self.col_name)    # 某种粒子强度和
        avg_ints = pd.DataFrame(np.nanmean(cleaned_df, axis=0).reshape(1,-1), columns=self.col_name)   # 某种粒子强度平均
        std_ints = pd.DataFrame(np.nanstd(cleaned_df, axis=0).reshape(1,-1), columns=self.col_name)    # 某种粒子强度的标准差
        basic_metric = pd.concat([short_name, min_ints, max_ints, count, sum_ints, avg_ints, std_ints], axis=0) 
        basic_metric.insert(0, 'metric', value=['ptc_name', 'min_ints', 'max_ints', 'count','sum_ints','avg_ints', 'std_ints'])
        basic_metric.set_index(['metric'],inplace=True)   # metric 列作为index
        file_name = 'basic_metric_' + self.ori_file_name
        basic_metric.to_csv(file_name)
        print('%s have been saved.' % file_name)
        return basic_metric


