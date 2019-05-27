# program to parse an address using nominatim api


# import libraries
import requests
import json

# PS : if you are going to automate the parsing 
#the server of nominatim has a limit of 1 request per second

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
        parsed_x[0]['address']
    flag=input("continue (y/n) - ")
 
