# program to geocode string using nominatim api(OSM based)
# modified to search in bengaluru region using bounding box method

# importing libraries
import requests
import json


# PS : if you are planning on automating the process 
# the server of nominatim has a limit of 1 request per second

flag="y"
while flag=="y" :
    text=input("enter address : ")
    text=text.split(",")
    text="+".join(text)
    text=text.replace(" ", "")
    
    #bounding coordinates added to restrict search results to city of banglore( approx)
    request = requests.get('https://nominatim.openstreetmap.org/?format=json&addressdetails=1&q='+text+'&format=json&limit=1&countrycodes=in&bounded=1&viewbox=76.9829,12.4578,78.2133,13.6491')

    # variable x is of type string.the size of empty result is 2 ( ie x=[]) 
    x=request.text
    if len(x)!= 2:
        parsed_x = json.loads(x)
        print ("latitude = ",parsed_x[0]['lat'],", longitude = ",parsed_x[0]['lon'])
    flag=input("continue (y/n) - ")
