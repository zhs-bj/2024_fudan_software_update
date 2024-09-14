#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
Courtesy of: iGEM 2022 Tsinghua, https://gitlab.igem.org/2022/software-tools/tsinghua
Adapted by: Hongchen Cheng
Date: 2024-08-19
"""

import numpy as np
from tqdm import tqdm
from gensim.models import word2vec
import logging


DATA_PATH = "/home/chc/fudan2024/similarity/kmer2vec/data/"
OUTPUT_PATH = "/home/chc/fudan2024/similarity/data/"
N = 70000

# Read in sequences

f=open(DATA_PATH+"seqdump.txt","r")
contents=f.read()

text=list(contents)

name=[[] for i in range(N)]
dna=[[] for i in range(N)]
n_seq=0    
i=0

while text[i]!='!':
    if text[i]=='>':
        m=1
        n_seq=n_seq+1
    else:
        m=0
    if m==1:
        j=i+1
        while text[j]!='\n':
            name[n_seq].append(text[j])
            j=j+1
        i=j
        m=0
    else:
        j=i
        while text[j]!='>' and text[j]!='!':
            if text[j]=='\n':
                j=j+1
            else:
                dna[n_seq].append(text[j])
                j=j+1
        i=j-1
    i=i+1
    
print(n_seq)

for i in range(1,n_seq+1):
    name[i] = ''.join(name[i])
    dna[i].append('!')

f.close()

# Separate sequences into k-mers

kmer=4

sentence=['' for i in range(N)]

for i in tqdm(range(1,n_seq+1)):
    for j in range(0,len(dna[i])-kmer):
        sentence[i] = ''.join(dna[i][j:j+kmer])

f=open(DATA_PATH+"sequence_separated.txt","w")

for i in tqdm(range(1,n_seq+1)):
    f.write(sentence[i]+' ')

f.close()

# Train word2vec model

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)  
sentences = word2vec.Text8Corpus(DATA_PATH+'sequence_separated.txt')  
model = word2vec.Word2Vec(sentences, sg=1,  window=24,  min_count=1,  negative=5, sample=0.001, hs=0, workers=1, epochs=1, vector_size=100, seed=0)  
model.save(DATA_PATH+'sequence_separated_word2vec.model') 

# Calculate sequence embeddings

model = word2vec.Word2Vec.load(DATA_PATH+'sequence_separated_word2vec.model')

word=[[] for i in range(N)]
for i in range(1,n_seq+1):
    word[i]=sentence[i].split()

v=[[] for i in range(N)]
vc=[[] for i in range(N)]
for i in range(1,n_seq+1):
    v[i]=np.zeros(100)
    vc[i]=np.zeros(100)
for ii in tqdm(range(1,n_seq+1)):
    for i in range(0,len(word[ii])):
        if word[ii][i] in model.wv.key_to_index.keys():
            v[ii]=v[ii]+np.array(model.wv[word[ii][i]]/len(word[ii]))
    for i in range(0,len(word[ii])):
        if word[ii][i] in model.wv.key_to_index.keys():
            vc[ii]=vc[ii]+np.array((model.wv[word[ii][i]]-v[ii])**2/len(word[ii]))

# Output sequence embeddings

vv=[[] for i in range(N)]
vv1=[[] for i in range(N)]
vv2=[[] for i in range(N)]

fout = open(OUTPUT_PATH + "seq_embeddings.txt", "w")

for i in range(1,n_seq+1):
    vv1[i]=np.array(v[i])
    vv2[i]=np.array(vc[i])
    vv[i]=np.hstack((vv1[i],vv2[i]))
    fout.write(name[i] + ':')
    fout.write(' '.join([f"{j}" for j in vv[i]]))
    fout.write('\n')

fout.close()