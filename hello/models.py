from django.db import models

class Drone(models.Model):
	serialNumber = models.TextField()
	pilotName    = models.TextField()
	pilotEmail   = models.TextField()
	pilotPhone   = models.TextField()
	positionX    = models.FloatField()
	positionY    = models.FloatField()
	closestTo    = models.FloatField()
	datetime     = models.DateTimeField()
	violatingNDZ  = models.BooleanField()
	lastViolated = models.FloatField()
