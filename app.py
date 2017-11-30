from flask import Flask, render_template, request
import kdtree
import pool
import json
import sms
treeOfCities=kdtree.create(dimensions=3);
dictMap={}
app = Flask(__name__)
@app.route('/api/reCaP/v1/consumer',methods=['POST'])
def addToPool():
	key=request.json["key"]["value"];
	pickupLat=request.json["PickUp"]["Latitude"];
	pickupLng=request.json["PickUp"]["Longitude"];
	DestLat=request.json["Destination"]["Latitude"];
	DestLng=request.json["Destination"]["Longitude"];
	pool.addPickUpToPool(pickupLat,pickupLng,key,treeOfCities,dictMap)
	pool.addDestToPool(DestLat,DestLng,key,treeOfCities,dictMap)
	return "Successful"
@app.route('/api/reCaP/v1/consumer/<id>',methods=['DELETE'])
def delFromPool(id):
	pickupLat=request.json["PickUp"]["Latitude"];
	pickupLng=request.json["PickUp"]["Longitude"];
	destLat=request.json["Destination"]["Latitude"];
	destLng=request.json["Destination"]["Longitude"];
	pool.delPickUpFromPool(pickupLat,pickupLng,int(id),treeOfCities,dictMap)
	pool.delDestFromPool(destLat,destLng,int(id),treeOfCities,dictMap)
	return "Successful";
@app.route('/api/reCaP/v1/rider/',methods=['POST'])
def getFromPool():
	key=request.json["key"]["value"];
	pickupLat=request.json["PickUp"]["Latitude"];
	pickupLng=request.json["PickUp"]["Longitude"];
	destLat=request.json["Destination"]["Latitude"];
	destLng=request.json["Destination"]["Longitude"];
	jsonResult=pool.getFromPool(pickupLat,pickupLng,destLat,destLng,treeOfCities,dictMap)
	try:
		phoneNumber=str(jsonResult["key"])
		message="Please contact "+ str(key)+ ". The driver will pick you up at the specified location."
		sms.sendSMS(phoneNumber,message)
		return json.dumps(jsonResult)
	except:
		return "No matching found",status.HTTP_500_INTERNAL_SERVER_ERROR
if __name__ == '__main__':
	#Creating the dictionary of Cities
	pool.createTreeOfCities(treeOfCities,dictMap)
	app.run(host='localhost',port="9090")

'''
Request JSON structure:
addtopool-post
POST
{
	'PickUp':{'Latitude':<lat>,'Longitude':<lng>},
	'Destination':{'Latitude':<lat>,'Longitude':<lng>},
	'key':{
		'name':'phone number',
		'value':<val>
	}

}

DELETE:
{
	'PickUp':{'Latitude':<lat>,'Longitude':<lng>},
	'Destination':{'Latitude':<lat>,'Longitude':<lng>},
	'numberOfPassengers': <no>
}

GET
{
	'PickUp':{'Latitude':<lat>,'Longitude':<lng>},
	'Destination':{'Latitude':<lat>,'Longitude':<lng>},
	'key':{
		'name':'phone number',
		'value':<val>
	}
}
'''