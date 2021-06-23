from geopy.distance import geodesic
import requests
import json
import geocoder
import time


def callStation():
    lat = (requests.get("http://api.open-notify.org/iss-now.json")
           ).json()['iss_position']['latitude']
    long = (requests.get("http://api.open-notify.org/iss-now.json")
            ).json()['iss_position']['longitude']
    g = geocoder.osm([lat, long], method='reverse')
    print(("Target acquired, tracking active: the location of the ISS is {}, {}.".format(
        lat, long))), print("Landmarks the station is visible from: ", g.country)
    print("See location: ", "http://www.google.com/maps/place/{},{}".format(lat, long))
    lastknown = (lat, long)
    return lastknown


def callDistance(lastknown, currentknown):
    print("ISS has traveled approximately ", geodesic(
        lastknown, currentknown).miles, "miles in 60 seconds.")
    print("ISS has traveled approximately ", geodesic(
        lastknown, currentknown).kilometers, "kilometers in 60 seconds.")
    return currentknown


def calcDistance(firstknown, currentknown):
    print("The ISS is traveling at approximately  ", geodesic(
        firstknown, currentknown).miles, "miles per minuite.")
    mile_hour = (int(geodesic(firstknown, currentknown).miles) * 60)
    print("The ISS is traveling at approximately ", mile_hour,
          " miles per hour.\n>>>discontinuing tracking>>>")
    print("The ISS is traveling at approximately  ", geodesic(
        firstknown, currentknown).kilometers, "kilometers per minuite.")
    kilometer_hour = (int(geodesic(firstknown, currentknown).kilometers) * 60)
    print("The ISS is traveling at approximately ", kilometer_hour,
          " kilometers per hour.\n>>>discontinuing tracking>>>")


data = (requests.get("http://api.open-notify.org/astros.json")).json()
print("Data Request: ", (data['message'])), print(
    "Total humans in orbit: ", data['number'], "\nPrinting manifest:")
for i in range(len(data['people'])):
    print(("%s is currently in space aboard the %s." %
           ((data['people'][i]['name']), (data['people'][i]['craft']))))
for i in range(6):
    if i < 1:
        lastknown = callStation()
        firstknown = lastknown
        time.sleep(60)
    elif i < 5:
        currentknown = callStation()
        lastknown = callDistance(lastknown, currentknown)
        time.sleep(60)

    elif i == 5:
        print("FINAL ROUND:")
        currentknown = callStation()
        calcDistance(firstknown, currentknown)
