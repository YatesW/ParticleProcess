# ParticleProcess
分类&颗粒数浓度计算
* `DataLoader.py`:对原始数据的一些列预处理
* `IterMethod.py`:传统迭代方法在该场景下的复现（文件系统重新进行了设计）
* `PoissonMethod.py`:泊松分类法的最终版本，已经可是实现满意分类结果，并对空间代价进行优化
* `PostProcess.py`:对分类后数据进行后处理，主要包括：减背景、筛选符合要求的粒子、计算传输率TE、计算颗粒数浓度等。
* `main_Poisson`:泊松分类法从预处理到分类，最后到后处理的完整执行脚本
* `jupyter.ipynb`:以上代码的jupyter版本，jupyter便于可视化。该版本中加入了一些画图功能便于进行对比
* `层级聚类_cluster_Poisson`:对泊松法分类结果进行层级聚类 (Hierarchical Clustering) 的代码，其中包含了可视化函数便于对比效果。（距离参数分别使用了欧氏距离和相关性）
* `particle_get_mass.ipynb`:对泊松分类得到的颗粒态粒子进行质量（质量分布）计算和主成分统计。

|  表头   | 表头  |
|  ----  | ----  |
| 单元格  | 单元格 |
| 单元格  | 单元格 |
