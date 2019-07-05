<p align="center">
<a href="http://iihs.co.in/" target="_blank">
        <img src="https://scontent.fblr2-1.fna.fbcdn.net/v/t1.0-9/23032454_1830219147007896_1806916759773118613_n.jpg?_nc_cat=110&_nc_oc=AQlIf8adiHXbxnuPNX_OlQptuPXR1f2eDpLZcS3DuA607MgYotJRqh1GcjUEAPX6fN4&_nc_ht=scontent.fblr2-1.fna&oh=c7f63c0b0099a7b2dfb06011d9b082a6&oe=5DAE5BD6" 
alt="IIHS LOGO" width="200" height="200" border="10" align="center"/></a>
</p>

## Indian Institute for Human Settlements Bangalore
[`IIHS`](http://iihs.co.in/) is a section 8 company under the Indian Companies Act, established in 2008 by eminent Indians who have distinguished themselves in various fields, including the government, private sector and civil society. 

The Repository consists of various programs and techniques that have been used or implemented in the main project [`Enterprise map of Bangalore`](https://www.peak-urban.org/project/mapping-bangalores-industrial-transformation)
***
```
    |-- EDA_on_geonames.ipynb
    |-- GUI_Tool_Geocode.ipynb
    |-- geocode_v_1.ipynb
    |-- geocode_v_2.ipynb
    |-- readme.md
    |-- Pincode
    |    |
    |    |-- Master_list_Pincodes_bangalore.ipynb
    |    |-- readme.md
    |    
    |-- REPORT
         |-- REPORT_SUB_TASK-1.docx
         |-- readme.md
         |-- routing.js
```
***
- ___EDA_on_geonames.ipynb___ - A first level Exploratory Data Analysis on [`Geonames`](https://www.geonames.org/).a short analysis on integrity of geodata available in the geonames repository against data obtained from google
- ___GUI_Tool_Geocode.ipynb___ - Python GUI created using PySimpleGui and [`Nominatim API`](http://nominatim.org/release-docs/latest/api/Overview/).the Interface loads a csv file from local machine and Geocodes data semi-manually and saves accordingly
- ___geocode_v_1.ipynb___ - An initial version of python program to geocode economic census data
- ___geocode_v_2.ipynb___ - modified version with minor bug fixes and optimised search options using bounding boxes
- ___Master_list_Pincodes_bangalore.ipynb___ - Program to create a master list of postal codes in Banglore urban and rural districts using various spatial techniques.the [`source file`](https://data.gov.in/) has been included in the directory.
