import requests
import json

# Hit Google's reverse geocoder directly
# NOTE: I *think* their terms state that you're supposed to
# use google maps if you use their api for anything.
def getSubLocality(latitude, longitude):
    base = "https://maps.googleapis.com/maps/api/geocode/json?"
    apiKey="AIzaSyBUefEqYeqNRRFzJAX39pTGYRqx_AqASm0"
    params = "latlng={lat},{lon}&key={key}&result_type=postal_code".format(
        lat=latitude,
        lon=longitude,
        key=apiKey
    )
    url = "{base}{params}".format(base=base, params=params)
    response = requests.get(url)
    #print json.dumps(response.json(), sort_keys=True, indent=4, separators=(',', ': '))
    return (response.json()['results'][0]['address_components'][0]["short_name"]);

#components=administrative_area:TX

def getSubLocalityLatLang(lat, lng):
    postal_code=getSubLocality(lat,lng)
    base = "https://maps.googleapis.com/maps/api/geocode/json?"
    apiKey="AIzaSyBUefEqYeqNRRFzJAX39pTGYRqx_AqASm0"
    params = "components=postal_code:{postal_code}&key={key}".format(
        postal_code=postal_code,
        key=apiKey
    )
    url = "{base}{params}".format(base=base, params=params)
    #print(url)
    response = requests.get(url)
    #print json.dumps(response.json(), sort_keys=True, indent=4, separators=(',', ': '))
    jsonloc= (response.json()['results'][0]['geometry']['location'])
    return [jsonloc['lat'],jsonloc['lng']]

#print(getSubLocalityLatLang(40.714224,-73.961452))