import pycrfsuite
from collections import Counter

tagger = pycrfsuite.Tagger()
tagger.open('blraddrparser/blraddr.crfsuite')

info = tagger.info()

def print_transitions(trans_features):
    for (label_from, label_to), weight in trans_features:
        print("%-6s -> %-7s %0.6f" % (label_from, label_to, weight))

print("Top likely transitions:")
print_transitions(Counter(info.transitions).most_common(15))

print("\nTop unlikely transitions:")
print_transitions(Counter(info.transitions).most_common()[-15:])

def print_state_features(state_features):
    for (attr, label), weight in state_features:
        print("%0.6f %-6s %s" % (weight, label, attr))

print("Top positive:")
print_state_features(Counter(info.state_features).most_common(20))

print("\nTop negative:")
print_state_features(Counter(info.state_features).most_common()[-20:])

import blraddrparser
from postal.parser import parse_address

addresses = ["No. 106, Skanda Complex, 10th Main, 2nd Stage, CMH Road, Indiranagar",
"No. 106, Skanda Complex, 10th Main, 2nd Stage, CMH Road, Indiranagar, Bangalore, 560075",
"No. 1, FG GANESH BUILDING, VISHWANATH NAGAR, NAGENAHALLI, R.T.NAGAR, BANGALORE NORTH, 560032",
"C403, Mantri Webcity, Near XLR8, Hennur Bagalur Road, Kothanur, Bangalore, PIN 560077",
"No. 6, PSS Plaza, Wind Tunnel Road, Murugeshpalya, Bangalore, 560017",
"16th Cross Rd, Sadashiva Nagar, Armane Nagar, Bengaluru, Karnataka, 560080",
"No. 61, KODUSANNAPPANA HALLI, KANNUR POST, HENNUR BAGALOOR MAIN ROAD, BIDARAHALLI HOBLI,BIDARAHALLI,560049",
"NO. 4,BANBUI GARDEN, GANGANAGARA,BANGALORE,560012",
"NO. 4024,SOBHA AMETHYST, SURVEY NO. 184, KANNAMANGALA, BIDARAHALLI ROAD,BIDARAHALLI,560067",
"NO 14/2, GROUND FLOOR, RAJESH CHAMBERS, BURTON CENTRE, BANGALORE,SHANTALA NAGAR,560001",
"No. 711, 7TH FLOOR, MITTAL TOWER B.VING, MG ROAD, BANGALORE, Halasur, 560001",
"NO.602,GROUND FLOOR, BEML LAYOUT, THUBARADAHALLI, BANGALORE,VARTHURU,560066",
"NO. 32/2,V MAIN ROAD, I FLOOR, CHAMRAJPET,BANGALORE,560018",
"NO. 596/1, 15TH CROSS, SAMPIGE MAIN ROAD, MALLESWARAM,BANGALORE",
"SHED NO. 4,VIRGONAGAR INDUSTRIAL AREA, OPP HP PETROL BUNK, VIRGONAGAR,AVALAHALLI,560049"
]

print("Custom:")
print("+++++++++++")
for add in addresses:
    print(add)
    print(blraddrparser.parse(add))

print("\n\nLibpostal:")
print("+++++++++++")
for add in addresses:
    print(add)
    print(parse_address(add))

