#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import numpy as np
import warnings

warnings.filterwarnings('ignore')



class PostProcess:

    def __init__(self, particle_csv, resolve_csv):
        '''
        particle_csv ：颗粒态数据csv文件名，放在当前目录下即可
        resolve_csv：溶解态数据csv文件名，放在当前目录下即可
        '''
        self.ptc_df = pd.read_csv(particle_csv)
        self.resl_df = pd.read_csv(resolve_csv)
        self.df_len = len(self.resl_df)
        self.col_name = self.ptc_df.columns


    def get_background(self):
        '''
        计算每种粒子的背景值并保存为csv
        '''
        BG = pd.DataFrame([np.nanmean(self.resl_df, axis=0)] * self.df_len, columns=self.col_name)
        return BG


    def substract_background(self):
        '''
        对颗粒态数据减去背景值并保存为csv
        background_df：背景值df
        '''
        BG = self.get_background()
        file_name = 'substract_bg_particle.csv'
        substract_bg_particle = self.ptc_df - BG
        substract_bg_particle.to_csv(file_name, index=None)
        print("%s have been saved." % file_name)


    def select_columns(self, final_particle_csv, target_particle):
        '''
        在减去背景的颗粒态数据中选择要处理的粒子，组成df并保存为csv
        final_particle_csv：减去背景后的颗粒态csv文件名，放在该目录下即可
        target_particle：要选择的粒子名，如:'Au'
        '''
        ptc_df = pd.read_csv(final_particle_csv)
        ptc_name_full_li = ptc_df.columns.tolist()  # 表头
        ptc_name_short_li = list(map(lambda x: x[-10:-8], ptc_name_full_li))  # 元素名
        select_col_li = []  # 选中元素所在列的完整列名

        for i in range(len(ptc_name_full_li)):
            if target_particle == ptc_name_short_li[i]:
                select_col_li.append(ptc_name_full_li[i])

        selected_ptc_df = pd.DataFrame(ptc_df, columns=select_col_li)
        file_name = target_particle + '_in_' + final_particle_csv
        selected_ptc_df.to_csv(file_name, index=None)
        print("%s particle have been selected." % target_particle)


    def get_particle_number_concentration(self, selected_particle_csv, TE, speed, CPS):
        '''
        ！！旧的颗粒数浓度计算方法！！

        计算去除背景后颗粒态的目标元素的颗粒数浓度。
        selected_particle_csv：减去背景后的颗粒态目标元素的csv文件名，放在该目录下即可
        TE：计算参数，手动输入
        speed：流速，手动输入
        CPS：目标粒子的单位CPS，手动输入
        '''
        ele_name = selected_particle_csv[0:2]
        selected_ptc_df = pd.read_csv(selected_particle_csv)
        ints_sum = pd.DataFrame(np.nansum(selected_ptc_df, axis=0).reshape(1, -1), columns=selected_ptc_df.columns)
        coef = 1000 / (2.5 * TE * speed * CPS)  # 强度和df要乘的系数
        ptc_num_concentration = coef * ints_sum
        file_name = ele_name + "_particle_number_concentration.csv"
        ptc_num_concentration.to_csv(file_name, index=None)
        print("The particle number concentration of %s have been computed." % ele_name)


    def get_TE(self, selected_particle_csv):
        '''
        利用Std文件减去背景值后的目标粒子数据，计算得到TE，并保存对应csv。
        selected_particle_csv：减去背景后的颗粒态目标元素的csv文件名，放在该目录下即可
        '''
        std_df = pd.read_csv(selected_particle_csv)  # std文件的df
        TE = pd.DataFrame((std_df.count()) / (2.5 * 0.02 * 1e6), columns=std_df.columns)
        TE.to_csv("TE.csv", index=None)
        print("TE have been computed.")


    def get_particle_number_con_new(self, selected_particle_csv, TE, speed):
        '''
        ！！新的的颗粒数浓度计算方法！！

        计算去除背景后颗粒态的目标元素的颗粒数浓度。
        selected_particle_csv：减去背景后的颗粒态目标元素的csv文件名，放在该目录下即可
        TE：计算参数，手动输入
        speed：流速，手动输入
        '''
        ele_name = selected_particle_csv[0:2]
        selected_ptc_df = pd.read_csv(selected_particle_csv)
        ptc_cnt = selected_ptc_df.count()
        coef = 1 / (2.5 * TE * speed)  # 粒子计数要乘的系数
        res = coef * ptc_cnt
        ptc_num_con = pd.DataFrame(res, columns=selected_ptc_df.columns)
        file_name = ele_name + "_particle_number_concentration.csv"
        ptc_num_con.to_csv(file_name, index=None)
        print("The particle number concentration of %s have been computed." % ele_name)
