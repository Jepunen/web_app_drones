import requests
from .models import Drone
from xml.etree import ElementTree as ET
from datetime import datetime as dt
from datetime import timedelta
import math

# Bird nest location
ORIGON_X, ORIGON_Y = 250_000, 250_000

# GET drone data and return XML element tree
def getDroneData():
    try:
        url = 'https://assignments.reaktor.com/birdnest/drones'
        r = requests.get(url=url)
        return ET.fromstring(r.content)
    except Exception as e:
        print(e)
        return None

# GET pilot information and return None (404) or pilot information
def getPilotInformation(serialNumber):
    try:
        url = 'https://assignments.reaktor.com/birdnest/pilots/' + serialNumber
        r = requests.get(url=url)
        if r.status_code == 404:
            return None
        else: 
            return r.json()
    except Exception as e:
        print(e)
        return None

# Receives the XML element tree and updates the data to DB
def updateDroneDataToDB(root):

    # Time of drone capture from XML
    time = root.find('capture')
    timeString = time.attrib['snapshotTimestamp']
    droneDatetime = dt.strptime(timeString, "%Y-%m-%dT%H:%M:%S.%f%z")
    timeNow = dt.now()

    newDrones = {}
    # New drones from XML -> Dictionary
    for drone in root.iter('drone'):
        newDrones[drone.find('serialNumber').text] = {
            'serialNumber': drone.find('serialNumber').text,
            'positionX': float(drone.find('positionX').text),
            'positionY': float(drone.find('positionY').text)
            }

    # Go through drones in DB
    for oldDrone in Drone.objects.all():
        if oldDrone.serialNumber in newDrones:
            # A spotted drone has been re-spotted
            updatedDrone = newDrones[oldDrone.serialNumber]

            if oldDrone.pilotName == 'N/A':
                # Pilot info not set, try updating it
                pilotInfo = getPilotInformation(oldDrone.serialNumber)
                if pilotInfo != None:
                    # GET for pilot info != 404
                    oldDrone.pilotName = f"{pilotInfo['lastName']} {pilotInfo['firstName']}"
                    oldDrone.pilotPhone = pilotInfo['phoneNumber']
                    oldDrone.pilotEmail = pilotInfo['email']

            # Update the drone location
            oldDrone.positionX = updatedDrone['positionX']
            oldDrone.positionY = updatedDrone['positionY']

            # Check if drone closer to nest than last time
            if oldDrone.closestTo > round(droneDisctanceFromNest(updatedDrone['positionX'], updatedDrone['positionY']) / 1000, 2):
                oldDrone.closestTo = round(droneDisctanceFromNest(updatedDrone['positionX'], updatedDrone['positionY']) / 1000, 2)

            # Update when the drone was seen
            oldDrone.datetime  = droneDatetime

            if isDroneViolatingNDZ(updatedDrone['positionX'], updatedDrone['positionY']):
                # Currently violating NDZ
                oldDrone.violatingNDZ = True
                oldDrone.lastViolated = float("%.1f" % round(((timeNow - droneDatetime.replace(tzinfo=None)).total_seconds() / 60), 1))
            else:
                # Currently not violating NDZ
                oldDrone.violatingNDZ = False

            # Remove the updated drone from new drones
            newDrones.pop(oldDrone.serialNumber)

        if timeNow > oldDrone.datetime.replace(tzinfo=None) + timedelta(minutes=10):
            # Drone was last spotted over 10 minutes ago
            oldDrone.delete()
        else:
            # Drone spotted less than 10 minutes ago
            oldDrone.lastViolated = round(((timeNow - oldDrone.datetime.replace(tzinfo=None)).total_seconds() / 60), 1)
            oldDrone.save()

    # Only new drones remain in newDrones
    for drone in newDrones:
        if not Drone.objects.filter(serialNumber=drone).exists():
            # Drone not in DB
            if isDroneViolatingNDZ(newDrones[drone]['positionX'], newDrones[drone]['positionY']):
                # Drone violating NDZ
                drone = newDrones[drone]
                pilotInfo = getPilotInformation(drone['serialNumber'])
                newDrone = {}

                if pilotInfo != None:
                    # Successfully got pilot info
                    newDrone['pilotName'] = f"{pilotInfo['lastName']} {pilotInfo['firstName']}"
                    newDrone['pilotPhone'] = pilotInfo['phoneNumber']
                    newDrone['pilotEmail'] = pilotInfo['email']
                else:
                    # 404 error while getting pilot info
                    newDrone['pilotName'] = 'N/A'
                    newDrone['pilotPhone'] = 'N/A'
                    newDrone['pilotEmail'] = 'N/A'

                # Create rest of newDrone
                newDrone['positionX']    = drone['positionX']
                newDrone['positionY']    = drone['positionY']
                newDrone['closestTo']    = round(droneDisctanceFromNest(drone['positionX'], drone['positionY']) / 1000, 2)
                newDrone['datetime']     = droneDatetime
                newDrone['lastViolated'] = round(((timeNow - droneDatetime.replace(tzinfo=None)).total_seconds() / 60), 1)
                newDrone['violatingNDZ'] = True
                newDrone['serialNumber'] = drone['serialNumber']

                addDroneToDB(newDrone)

    return None

# Calculate drone distance from nest using pythagoras theorem
def droneDisctanceFromNest(X, Y):
    try:
        return math.hypot(ORIGON_X - X, ORIGON_Y - Y)
    except Exception as e:
        print(e)
        return 0

# Calculate if drone is in the 100m radius circle from the nest
def isDroneViolatingNDZ(X, Y):
    try:
        return (X - 250_000)**2 + (Y - 250_000)**2 < 100_000**2
    except Exception as e:
        print(e)
        return False

# Empty the DB, comment out in views to use
def clearDBOfDrones():
    Drone.objects.all().delete()

# Add a drone to the DB
def addDroneToDB(drone):
    try:
        pilotName  = drone['pilotName']
        pilotEmail = drone['pilotEmail']
        pilotPhone = drone['pilotPhone']
        positionX  = drone['positionX']
        positionY  = drone['positionY']
        closestTo  = drone['closestTo']
        datetime   = drone['datetime']
        violatingNDZ  = drone['violatingNDZ']
        lastViolated = drone['lastViolated']
        serialNumber = drone['serialNumber']

        Drone.objects.create(
            serialNumber=serialNumber,
            pilotName=pilotName,
            pilotEmail=pilotEmail,
            pilotPhone=pilotPhone,
            positionX=positionX,
            positionY=positionY,
            closestTo=closestTo,
            violatingNDZ=violatingNDZ,
            lastViolated=lastViolated,
            datetime=datetime,
        )
        
    except Exception as e:
        print('An error occured while adding drone to DB')
        print(e)

    return None