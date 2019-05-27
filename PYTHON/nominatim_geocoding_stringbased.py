# program to geocode a address or place using nominatim api based on open street maps 

# importing libraries
import requests
import time
import json


flag="y"
while flag=="y" :
    text=input("enter address : ")
    text=text.split(",")
    text="+".join(text)
    text=text.replace(" ", "")
    request = requests.get('https://nominatim.openstreetmap.org/?format=json&addressdetails=1&q='+text+'&format=json&limit=1')
    x=request.text
    #print (x)
    if len(x)!= 0 :
        parsed_x = json.loads(x)
        print ("latitude = ",parsed_x[0]['lat'],", longitude = ",parsed_x[0]['lon'])
    flag=input("continue (y/n) - ")
