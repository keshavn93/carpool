import pandas as pd
import numpy as np
import kdtree
import geoCode
import json
def createTreeOfCities(treeOfCities,dictMap):
	names=['zipcode','lat','lang']
	df = pd.read_csv('zips.csv', header=None, names=names)
	df.head()
	x = np.array(df.ix[1:,:])
	for iter in x:
		for pin in iter[0].split(' '):
			treeOfCities.add((float(iter[1]),float(iter[2]),int(pin)))
			dictMap={int(pin):{'pickup':kdtree.create(dimensions=3),'dest':kdtree.create(dimensions=3)}}

def addPickUpToPool(lat,lng,key,treeOfCities,dictMap):
	arr=treeOfCities.search_knn((float(lat),float(lng),int(geoCode.getSubLocality(lat,lng))),2)#returns array of size 2 having nodes of type item
	for datum,dist in arr:
		l1,l2,data=datum.data
		localTree=None
		try:
			localTree=dictMap[data]['pick_up']
		except:
			localTree=kdtree.create(dimensions=3)
		localTree.add((lat,lng,key))
		#to update the hashMap
		try:
			trees=dictMap[data]
			trees['pick_up']=localTree
			dictMap[data]=trees
		except:
			dictMap[data]={'pickup':localTree,'dest':kdtree.create(dimensions=3)}

def delPickUpFromPool(lat,lng,key,treeOfCities,dictMap):
	arr=treeOfCities.search_knn((float(lat),float(lng),int(geoCode.getSubLocality(lat,lng))),2)#returns array of size 2 having nodes of type item
	for datum,dist in arr:
		l1,l2,data=datum.data
		localTree=dictMap[data]['pick_up']
		localTree._remove((lat,lng,key))
		#to update the hashMap
		trees=dictMap[data]
		trees['pickup']=localTree
		dictMap[data]=trees

def addDestToPool(lat,lng,key,treeOfCities,dictMap):
	arr=treeOfCities.search_knn((float(lat),float(lng),int(geoCode.getSubLocality(lat,lng))),2)#returns array of size 2 having nodes of type item
	for datum,dist in arr:
		l1,l2,data=datum.data
		localTree=None
		try:
			localTree=dictMap[data]['dest']
		except:
			localTree=kdtree.create(dimensions=3)
		localTree.add((lat,lng,key))
		#to update the hashMap
		try:
			trees=dictMap[data]
			trees['dest']=localTree
			dictMap[data]=trees
		except:
			dictMap[data]={'dest':localTree,'pickup':kdtree.create(dimensions=3)}

def delDestFromPool(lat,lng,key,treeOfCities,dictMap):
	arr=treeOfCities.search_knn((float(lat),float(lng),int(geoCode.getSubLocality(lat,lng))),2)#returns array of size 2 having nodes of type item
	for datum,dist in arr:
		l1,l2,data=datum.data
		localTree=dictMap[data]['dest']
		localTree._remove((lat,lng,key))
		#to update the hashMap
		trees=dictMap[data]
		trees['dest']=localTree
		dictMap[data]=trees

def getFromPool(lat1,lng1,lat2,lng2,treeOfCities,dictMap):
	ans=[]
	listofKeys=[]
	resultPickUpArr=[]
	resultDestArr=[]
	arr=treeOfCities.search_knn((float(lat1),float(lng1),int(geoCode.getSubLocality(lat1,lng1))),2)#returns array of size 2 having nodes of type item
	for datum,dist in arr:
		l1,l2,data=datum.data
		localTree=None
		try:
			localTrees=dictMap[data]
		except:
			continue;#doesn't exist in this
		pickUp=localTrees['pickup'].search_knn((lat1, lng1,0),10)
		for node in pickUp:
			resultPickUpArr.append(node)
	arr=treeOfCities.search_knn((float(lat2),float(lng2),int(geoCode.getSubLocality(lat2,lng2))),2)#returns array of size 2 having nodes of type item
	for datum,dist in arr:
		l1,l2,data=datum.data
		localTree=None
		try:
			localTrees=dictMap[data]
		except:
			continue;#doesn't exist in this
		dest=localTrees['dest'].search_knn((lat2, lng2,0),10)
		for node in dest:
			resultDestArr.append(node)
	if(len(resultPickUpArr)==0 or len(resultDestArr)==0):
		return ''
	else:
		for (vals,c) in resultPickUpArr:
			a1,b1,d1=vals.data
			for (destVals,e) in resultDestArr:
				a2,b2,d2=destVals.data
				if(d1==d2):
					if d1 in listofKeys:
						continue;
					ans.append( {'pickup':vals.data,'dest':destVals.data,'total_distance':(c+e),'key':d1})
					listofKeys.append(d1)
	mindist=0;
	min=None;
	for elts in ans:
		if(elts["total_distance"]>mindist):
			min=elts
			mindist=elts["total_distance"]
	return min



