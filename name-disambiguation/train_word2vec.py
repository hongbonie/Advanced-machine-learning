# 保存下载的实验数据中的文本，并使用这些文本训练词向量 
## SAVE all text in the datasets

import codecs
import json
from os.path import join
import pickle
import os
import re


pubs_raw = load_json("train","train_pub.json")
pubs_raw1 = load_json("sna_data","sna_valid_pub.json")
pubs_raw2 = load_json("sna_test_data","test_pub_sna.json")
r = '[!“”"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~—～’]+'
f1 = open ('gene/all_text.txt','w',encoding = 'utf-8')

for i,pid in enumerate(pubs_raw):
    pub = pubs_raw[pid]
    
    for author in pub["authors"]:
        if "org" in author:
                org = author["org"]
                pstr = org.strip()
                pstr = pstr.lower()
                pstr = re.sub(r,' ', pstr)
                pstr = re.sub(r'\s{2,}', ' ', pstr).strip()
                f1.write(pstr+'\n')
            
    title = pub["title"]
    pstr=title.strip()
    pstr = pstr.lower()
    pstr = re.sub(r,' ', pstr)
    pstr = re.sub(r'\s{2,}', ' ', pstr).strip()
    f1.write(pstr+'\n')
    
    if "abstract" in pub and type(pub["abstract"]) is str:
        abstract = pub["abstract"]
        pstr=abstract.strip()
        pstr = pstr.lower()
        pstr = re.sub(r,' ', pstr)
        pstr = re.sub(r'\s{2,}', ' ', pstr).strip()
        f1.write(pstr+'\n')
        
    venue = pub["venue"]
    pstr=venue.strip()
    pstr = pstr.lower()
    pstr = re.sub(r,' ', pstr)
    pstr = re.sub(r'\s{2,}', ' ', pstr).strip()
    f1.write(pstr+'\n')
    
for i,pid in enumerate(pubs_raw1):
    pub = pubs_raw1[pid]
    
    for author in pub["authors"]:
        if "org" in author:
                org = author["org"]
                pstr = org.strip()
                pstr = pstr.lower()
                pstr = re.sub(r,' ', pstr)
                pstr = re.sub(r'\s{2,}', ' ', pstr).strip()
                f1.write(pstr+'\n')
            
    title = pub["title"]
    pstr=title.strip()
    pstr = pstr.lower()
    pstr = re.sub(r,' ', pstr)
    pstr = re.sub(r'\s{2,}', ' ', pstr).strip()
    f1.write(pstr+'\n')
    
    if "abstract" in pub and type(pub["abstract"]) is str:
        abstract = pub["abstract"]
        pstr=abstract.strip()
        pstr = pstr.lower()
        pstr = re.sub(r,' ', pstr)
        pstr = re.sub(r'\s{2,}', ' ', pstr).strip()
        f1.write(pstr+'\n')
        
    venue = pub["venue"]
    pstr=venue.strip()
    pstr = pstr.lower()
    pstr = re.sub(r,' ', pstr)
    pstr = re.sub(r'\s{2,}', ' ', pstr).strip()
    f1.write(pstr+'\n')


for i,pid in enumerate(pubs_raw2):
    pub = pubs_raw2[pid]
    
    for author in pub["authors"]:
        if "org" in author:
                org = author["org"]
                pstr = org.strip()
                pstr = pstr.lower()
                pstr = re.sub(r,' ', pstr)
                pstr = re.sub(r'\s{2,}', ' ', pstr).strip()
                f1.write(pstr+'\n')
            
    title = pub["title"]
    pstr=title.strip()
    pstr = pstr.lower()
    pstr = re.sub(r,' ', pstr)
    pstr = re.sub(r'\s{2,}', ' ', pstr).strip()
    f1.write(pstr+'\n')
    
    if "abstract" in pub and type(pub["abstract"]) is str:
        abstract = pub["abstract"]
        pstr=abstract.strip()
        pstr = pstr.lower()
        pstr = re.sub(r,' ', pstr)
        pstr = re.sub(r'\s{2,}', ' ', pstr).strip()
        f1.write(pstr+'\n')
        
    venue = pub["venue"]
    pstr=venue.strip()
    pstr = pstr.lower()
    pstr = re.sub(r,' ', pstr)
    pstr = re.sub(r'\s{2,}', ' ', pstr).strip()
    f1.write(pstr+'\n')
        
        
f1.close()