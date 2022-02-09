from DataLoader import DataLoader
from IterMethod import IterMethod
from PoissonMethod import PoissonMethod
from PostProcess import PostProcess



# 泊松法执行完整流程

# 超参数
origin_csv = 'data_1.csv'   # 原始数据的csv文件
credible = 0.7              # 泊松分布的置信度

TE_flag = True              # 是否计算TE

TE = 0.30426                # TE
speed = 0.02                # 流速


def main():
    if TE_flag:  # 计算TE
        #  一：执行
        data_loader = DataLoader(origin_csv)                        # 实例化
        cleaned_data = data_loader.get_cleaned_data()               # 得到清洗后的数据
        metric_data = data_loader.get_basic_metirct(cleaned_data)   # 得到相关指标统计结果

        # 二：Poisson执行
        poissonmethod = PoissonMethod(cleaned_data, metric_data, credible)   # 实例化
        avgints_lambda_scale = poissonmethod.normal_lambda()                 # 得到与lambda相关参数组成的csv
        intensity_threshold = poissonmethod.get_ints_thr()                   # 经过泊松过程得到强度阈值的csv
        poissonmethod.classifier()                                           # 分类得到颗粒态和溶解态数据csv

        # 三：执行
        p_process = PostProcess('Poisson_particle.csv', 'Poisson_resolve.csv')    # 实例化
        p_process.substract_background()                                          # 颗粒态数据减背景
        p_process.select_columns('substract_bg_particle.csv', 'Au')               # 在减背景后的颗粒态数据选择Au
        p_process.get_TE('Au_in_substract_bg_particle.csv')                       # 计算TE



    else:   # 计算颗粒数浓度
        #  一：执行
        data_loader = DataLoader(origin_csv)                        # 实例化
        cleaned_data = data_loader.get_cleaned_data()               # 得到清洗后的数据
        metric_data = data_loader.get_basic_metirct(cleaned_data)   # 得到相关指标统计结果

        # 二：Poisson执行
        poissonmethod = PoissonMethod(cleaned_data, metric_data, credible)  # 实例化
        avgints_lambda_scale = poissonmethod.normal_lambda()                # 得到与lambda相关参数组成的csv
        intensity_threshold = poissonmethod.get_ints_thr()                  # 经过泊松过程得到强度阈值的csv
        poissonmethod.classifier()                                          # 分类得到颗粒态和溶解态数据csv

        # 三：执行
        p_process = PostProcess('Poisson_particle.csv', 'Poisson_resolve.csv')                    # 实例化
        p_process.substract_background()                                                          # 颗粒态数据减背景
        p_process.select_columns('substract_bg_particle.csv', 'Au')                               # 在减背景后的颗粒态数据选择Au
        p_process.get_particle_number_con_new('Au_in_substract_bg_particle.csv', TE, speed)       # 计算Au的颗粒数浓度


if __name__ == '__main__':
    main()