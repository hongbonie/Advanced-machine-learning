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

## Homework_6: Social Influence Prediction With GNNS 

##### 作业说明
- 基于论文《DeepInf: Social Influence Prediction with Deep Learning》 实现对微博用户的行为进行预测，
- GCN (Graph Convolutional Network) and GAT (Graph attention network)
- 主要参考 ： https://github.com/xptree/DeepInf ，来实现模型预测 。 
- code ：homework_6
###### Data Set 
- adjacency_matrix.npy   每个实例对应的邻接矩阵， 每个实例是一个采样的自我中心网络。
- vertex_id.npy   自我中心网络的采样节点， 每一个节点由一个节点ID标识。
- deepwalk.emb_64   每个节点的预训练嵌入，每个嵌入向量都与一个节点ID相关联。
- vertex_feature.npy  每个节点的自定义顶点特征，每个嵌入向量都与一个节点ID相关联 。
- influence_feature.npy  自我中心网络的两个虚拟特征，一个指示用户是否活跃，另一个指示用户是否为自我 。 
- label.npy  每个实例的对应标签 

##### 论文模型复现解读
- 论文提出了端到端模型Deepinf，通过使用深度学习算法对图结构中节点影响力进行预测。 
- 论文主要解决的问题是：给定节点v， 和它的近邻节点，在一个时间窗口内，通过对开始时间各节点状态（包括图结构和节点特征）进行建模，完成对结束时间节点v状态的预测。 
- 在论文中，图结构使用图神经网络GCN（Graph Convolutional Neural Network）抽取，节点特征使用训练好的DeepWalk工具进行抽取。
- 在此基础上，使用注意力机制，通过对节点v临近的不同节点赋予不同的权重，使用图注意力网络GAT（Graph Attention Model）进行了进一步拓展。
- GCN执行图卷积运算，GAT则是在GCN的基础上加入了attention机制，能够在临近节点的影响中加入权重，从而能够将临近节点的影响进行差异化。
- 通过结合网络的结构特征和用户层面的特征信息，使用图卷积神经网络进行了学习 ；

## Homework_7:Semi-GAN: semi-supervised learning with GANs

##### 作业说明
- 基于论文《Semi-supervised Learning on Graphs with Generative Adversarial Nets》 实现在 cora 数据集上的分类。 

##### homework  
- 半监督学习：使用小的标记数据和大的未标记数据进行学习。
- 在semi-GAN中，鉴别器为分类器 
- 对与未标记的样本，鉴别器被训练为两类  fake real
- 对于标记样本，鉴别器被训练为识别N+1个类，（N个预定义类和一个附加类，指示图像是否为 fake）
- 论文 ： 使用生成对抗网络对图进行半监督学习。
- 在 cora 数据集上实现 GrapSGAN 
- 结果对比 
- 分析不同损失的影响 

###### Data Set 

Dataset | nodes  | edges | features | classses | labeled data 
---  |---   | ---  | --- |--- |---
Cora | 2708 | 5429 | 1433 | 7 | 140 






