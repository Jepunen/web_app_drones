from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from .models import Drone
from .scripts import getDroneData, updateDroneDataToDB, clearDBOfDrones

def home(request):        
    return render(request, 'hello/index.html')

def getDronesFromDB(requests):
    drones = list(Drone.objects.all().values())
    args = {
        'drones': drones,
    }
    return JsonResponse(args)

def getNewDrones(request):
    newDataXML = getDroneData()

    if newDataXML != None:
        # Data received successfully
        updateDroneDataToDB(newDataXML)

    #clearDBOfDrones()
    return HttpResponse()