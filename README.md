# Advanced-machine-learning
the project is where my homework submit which class is  Tsinghua Advanced machine learning .

## Homework_2
相关CODE和具体的报告说明见 name-disambiguation 文件夹
#### Name Disambiguation   同名消歧
- 同名消歧是一个具有挑战性的问题，由于数据的杂乱以及同名情景十分复杂，要快速且准确的解决同名消歧问题还有很大的障碍。 

#####  论文的冷启动消歧 
##### job-describe 
- 给定一堆拥有同名作者的论文，要求返回一组论文聚类，使得一个聚类内部的论文都是一个人的，不同聚类间的论文论文不属于一个人。最终目的是识别出那些同名作者的论文属于同一个人。 

##### tips 
- 可以把问题看成是对论文集的聚类任务，对于某个待消歧的人名，先提取出论文的特征向量，然后计算出论文之间的相似度矩阵。最后根据相似度矩阵利用聚类算法将论文划分成不同的簇，每一个簇代表一个作者的论文集。
- 主要难点在于怎么提取论文的特征向量，以及采用哪种聚类算法进行聚类。  
- 文本特征如何提取 ： TF-IDF ， 图表征的学习方法
- 聚类算法 ： DBSCAN算法  



