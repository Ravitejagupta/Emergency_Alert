# -*- coding: utf-8 -*-
"""
Created on Thu Aug 10 22:07:31 2017

@author: ravit
"""

# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn import datasets
from mpl_toolkits.mplot3d import Axes3D
import json
import pandas as pd


dataset = []
allData = []
header = []
with open('dataset.csv') as f:
    lines = f.readlines()
    header = lines[0].split(',')
    lines = lines[1:]
    for line in lines:
        allData.append([float(x) for x in line.split(',')[:5]])
        dataset.append([float(x) for x in line.split(',')[2:5]])
        
o_dataset = np.array(dataset)
print(o_dataset)    

X = o_dataset[:,0] ##numpy columns
Y = o_dataset[:,1]
Z = o_dataset[:,2]
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d') ##subplot initialisation
#
#ax.scatter(X, Y, Z, c='r', marker='o')
nb_clusters = 3
colors = ["g","r","b"]
kmeans = KMeans(n_clusters=nb_clusters)
kmeans.fit(o_dataset)

centriods = kmeans.cluster_centers_
labels = kmeans.labels_

##### 
clusters = []
clusters_issues = []
for c in range(nb_clusters):
    clusters.append([])   ##only for plotting
    clusters_issues.append([]) ##for json

for c in range(nb_clusters):
    for i in range(len(o_dataset)):
        if labels[i]==c:
            clusters[c].append(o_dataset[i])
            clusters_issues[c].append(allData[i])
            

########
##### 
resultDict = {}
counter = 0
for cluster in clusters_issues:
    df = pd.DataFrame(cluster, columns=header,index=['row_{0}'.format(x) for x in range(len(cluster))])
    df = df.transpose()
    jsonObject = df.to_dict()
    resultDict["cluster{0}".format(counter)] = jsonObject
    counter+=1

out_json = json.dumps(resultDict)
print(out_json)
########

###for plotting

counter = 0
for cluster in clusters:
    print(cluster)
    data = np.array(cluster)
    X = data[:,0]
    Y = data[:,1]
    Z = data[:,2]
    ax.scatter(X, Y, Z, c=colors[counter], marker='o')
    counter+=1
ax.scatter(centriods[:,0],centriods[:,1],centriods[:,2], c = 'black', marker='x')
plt.show()

print(header)
#plt.show()
#print("ravi")