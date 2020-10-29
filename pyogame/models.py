from django.contrib.auth.models import User
from django.db import models


class Lobby(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(max_length=30, null=True)
    password = models.CharField(max_length=30, null=True)
    token = models.CharField(max_length=50, null=True)
    auth = models.BooleanField(default=False)


class Universum(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=10, null=True)
    rank = models.IntegerField(null=True)
    blocked = models.BooleanField(null=True)


class Buildings(models.Model):
    metal_mine = models.IntegerField(null=True, default=0)
    crystal_mine = models.IntegerField(null=True, default=0)
    deuterium_mine = models.IntegerField(null=True, default=0)
    solar_plant = models.IntegerField(null=True, default=0)
    fusion_plant = models.IntegerField(null=True, default=0)
    metal_storage = models.IntegerField(null=True, default=0)
    crystal_storage = models.IntegerField(null=True, default=0)
    deuterium_storage = models.IntegerField(null=True, default=0)
    robotics_factory = models.IntegerField(null=True, default=0)
    shipyard = models.IntegerField(null=True, default=0)
    research_laboratory = models.IntegerField(null=True, default=0)
    alliance_depot = models.IntegerField(null=True, default=0)
    missile_silo = models.IntegerField(null=True, default=0)
    nanite_factory = models.IntegerField(null=True, default=0)
    terraformer = models.IntegerField(null=True, default=0)
    repair_dock = models.IntegerField(null=True, default=0)
    moon_base = models.IntegerField(null=True, default=0)
    sensor_phalanx = models.IntegerField(null=True, default=0)
    jump_gate = models.IntegerField(null=True, default=0)


class Ships(models.Model):
    small_transporter = models.IntegerField(null=True, default=0)
    large_transporter = models.IntegerField(null=True, default=0)
    colonyShip = models.IntegerField(null=True, default=0)
    recycler = models.IntegerField(null=True, default=0)
    light_fighter = models.IntegerField(null=True, default=0)
    heavy_fighter = models.IntegerField(null=True, default=0)
    cruiser = models.IntegerField(null=True, default=0)
    battleship = models.IntegerField(null=True, default=0)
    interceptor = models.IntegerField(null=True, default=0)
    bomber = models.IntegerField(null=True, default=0)
    destroyer = models.IntegerField(null=True, default=0)
    deathstar = models.IntegerField(null=True, default=0)
    reaper = models.IntegerField(null=True, default=0)
    explorer = models.IntegerField(null=True, default=0)
    espionage_probe = models.IntegerField(null=True, default=0)


class Defences(models.Model):
    rocket_launcher = models.IntegerField(null=True, default=0)
    laser_cannon_light = models.IntegerField(null=True, default=0)
    laser_cannon_heavy = models.IntegerField(null=True, default=0)
    gauss_cannon = models.IntegerField(null=True, default=0)
    ion_cannon = models.IntegerField(null=True, default=0)
    plasma_cannon = models.IntegerField(null=True, default=0)
    shield_dome_small = models.IntegerField(null=True, default=0)
    shield_dome_large = models.IntegerField(null=True, default=0)
    missile_interceptor = models.IntegerField(null=True, default=0)
    missile_interplanetary = models.IntegerField(null=True, default=0)


class Celestial(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    coordintate = models.CharField(max_length=30)
    universum = models.CharField(max_length=30, null=True)
    name = models.CharField(max_length=30, null=True)
    metal = models.CharField(max_length=30, null=True)
    crystal = models.CharField(max_length=30, null=True)
    deuterium = models.CharField(max_length=30, null=True)
    energy = models.CharField(max_length=30, null=True)
    ships = models.ForeignKey(Ships, null=True, on_delete=models.CASCADE)
    defences = models.ForeignKey(Defences, null=True, on_delete=models.CASCADE)
    buildings = models.ForeignKey(Buildings, null=True, on_delete=models.CASCADE)


class BotSettings(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    universum = models.CharField(max_length=30, null=True)
    repeat = models.IntegerField(null=True)
    nextRepeat = models.DateTimeField(null=True, auto_now=False, auto_now_add=False)
    active = models.BooleanField(null=True)
    base = models.CharField(max_length=20, null=True)
    saiver = models.BooleanField(null=True)
    expedition = models.BooleanField(null=True)
    expeditionFleet = models.ForeignKey(Ships, null=True, related_name='expeditionFleet', on_delete=models.CASCADE)
    collector = models.BooleanField(null=True)
    collectorTime = models.TimeField(auto_now=False, auto_now_add=False, null=True)
    raider = models.BooleanField(null=True)
    raiderFleet = models.ForeignKey(Ships, null=True, related_name='raiderFleet', on_delete=models.CASCADE)
    builder = models.BooleanField(null=True)
    builderFleet = models.ForeignKey(Ships, null=True, related_name='builderFleet', on_delete=models.CASCADE)
    builderDefences = models.ForeignKey(Defences, null=True, on_delete=models.CASCADE)


class BotLogger(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=100, null=True)


class Forum(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now=True)
    message = models.CharField(max_length=100, null=True)
