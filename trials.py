import pandas as pd
import numpy as np
import kdtree
import geoCode
import json
import pool
j=0;
treeOfCities=kdtree.create(dimensions=3);
dictMap={}
pool.createTreeOfCities(treeOfCities,dictMap)
names=['zipcode','lat','lang']
df = pd.read_csv('zips.csv', header=None, names=names)
df.head()
x = np.array(df.ix[1:200,:])
for iter in x:
	for pin in iter[0].split(' '):
		for i in range(0,15):
			try:
				pool.addPickUpToPool(float(iter[1])+(2*i/1000.0),float(iter[2])+(2*i/1000.0),pin,treeOfCities,dictMap)
				pool.addDestToPool(float(iter[1])+(0.002*(i+1)),float(iter[2])+(0.02*(i+1)),pin,treeOfCities,dictMap)
				j=(int(j)+1);
				print (pin)
			except:
				continue
			
			
				

print(pool.getFromPool(38.048677,-78.512815,38.03133,-78.51263,treeOfCities,dictMap))