import json 
import numpy as np 
import matplotlib.pyplot as plt 
from collections import defaultdict 

# 训练集分析
train_row_data_path = 'train/train_author.json'
train_pub_data_path = 'train/train_pub.json'

train_pub_data = json.load(open(train_pub_data_path, 'r', encoding='utf-8'))
train_data = json.load(open(train_row_data_path, 'r', encoding='utf-8'))
authors = [author for author in train_data]
authors_num_person = [len(train_data[author].keys()) for author in train_data] 

print('训练集同名数量：', len(authors))
print('消歧后实际作者数量：',  sum(authors_num_person))

# 绘制训练集同名作者个体数量
plt.figure(figsize=(40, 8), dpi=80)
x = range(len(authors))

plt.bar(x, authors_num_person, width=0.5)
plt.xticks(x, authors)
plt.xticks(rotation=270) 
plt.xlabel('训练集同名作者')
plt.ylabel('该名字同名作者数量（个）')
for xl, yl in zip(x, authors_num_person):
    plt.text(xl, yl+0.3, str(yl), ha='center', va='bottom', fontsize=10.5) 

mean_person = int(np.mean(authors_num_person))
plt.gca().hlines(mean_person,-1,225,linestyles='--',colors='red',label='平均值')
plt.annotate(u"平均值:" + str(mean_person), xy = (225, mean_person), xytext = (225, mean_person+40),arrowprops=dict(facecolor='red',shrink=0.1,width=2))

plt.show()

# print(len(authors))
# for author in train_data:
#     author_ids = train_data[author].keys()
#     print(author)
#     print(len(author_ids))