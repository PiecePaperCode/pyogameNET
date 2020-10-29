from pyogame.services.empire import settings
from django.shortcuts import render, redirect
from pyogame.models import Lobby, Celestial, Ships, BotLogger, Defences, Buildings
from ogame import OGame
from pyogame import services


def login(request, universum):
    lobby = Lobby.objects.get(user=request.user)
    empire = OGame(universum,
                   lobby.email,
                   services.encryption.decrypt(lobby.password),
                   proxy=services.proxy.randomProxy(),
                   token=lobby.token)
    lobby.token = empire.token
    lobby.save()
    return empire


def view(request, universum, message=None):
    celestials = Celestial.objects.filter(
            user=request.user,
            universum=universum
    ).order_by('coordintate')
    for celestial in celestials:
        celestial.coordintate = eval(celestial.coordintate)
    logger = BotLogger.objects.filter(user=request.user)[::-1][:30]
    data = {'universum': universum, 'celestials': celestials, 'logger': logger, 'message': message}
    return render(request, 'empire/empireview.html', data)


def celestial(request, universum):
    empire = login(request, universum)
    ids = empire.planet_ids() + empire.moon_ids()
    for i, id in enumerate(ids):
        celestial, new = Celestial.objects.get_or_create(
            user=request.user,
            universum=universum,
            coordintate=str(empire.celestial_coordinates(id)),
            name=(empire.planet_names() + empire.moon_names())[i]
        )
        resources = empire.resources((id))
        celestial.metal = str(services.formatting.large_int(resources.metal))
        celestial.crystal = str(services.formatting.large_int(resources.crystal))
        celestial.deuterium = str(services.formatting.large_int(resources.deuterium))
        celestial.energy = str(services.formatting.large_int(resources.energy))
        celestial.save()
    return redirect('empireView', universum)


def ship(request, universum):
    empire = login(request, universum)
    ids = empire.planet_ids() + empire.moon_ids()
    for i, id in enumerate(ids):
        celestial, new = Celestial.objects.get_or_create(
            user=request.user,
            universum=universum,
            coordintate=str(empire.celestial_coordinates(id)),
            name=(empire.planet_names() + empire.moon_names())[i]
        )
        if celestial.ships_id is not None:
            Ship = Ships(pk=celestial.ships.id)
        else:
            Ship = Ships()
        ships = empire.ships(id)
        Ship.small_transporter = ships.small_transporter.amount
        Ship.large_transporter = ships.large_transporter.amount
        Ship.colonyShip = ships.colonyShip.amount
        Ship.recycler = ships.recycler.amount
        Ship.light_fighter = ships.light_fighter.amount
        Ship.heavy_fighter = ships.heavy_fighter.amount
        Ship.cruiser = ships.cruiser.amount
        Ship.battleship = ships.battleship.amount
        Ship.interceptor = ships.interceptor.amount
        Ship.bomber = ships.bomber.amount
        Ship.destroyer = ships.destroyer.amount
        Ship.deathstar = ships.deathstar.amount
        Ship.reaper = ships.reaper.amount
        Ship.explorer = ships.explorer.amount
        Ship.espionage_probe = ships.espionage_probe.amount
        Ship.save()
        celestial.ships = Ship
        celestial.save()
    return redirect('empireView', universum)


def defence(request, universum):
    empire = login(request, universum)
    ids = empire.planet_ids() + empire.moon_ids()
    for i, id in enumerate(ids):
        celestial, new = Celestial.objects.get_or_create(
            user=request.user,
            universum=universum,
            coordintate=str(empire.celestial_coordinates(id)),
            name=(empire.planet_names() + empire.moon_names())[i]
        )
        if celestial.defences_id is not None:
            Defence = Defences(pk=celestial.defences.id)
        else:
            Defence = Defences()
        defences = empire.defences(id)
        Defence.rocket_launcher = defences.rocket_launcher.amount
        Defence.laser_cannon_light = defences.laser_cannon_light.amount
        Defence.laser_cannon_heavy = defences.laser_cannon_heavy.amount
        Defence.gauss_cannon = defences.gauss_cannon.amount
        Defence.ion_cannon = defences.ion_cannon.amount
        Defence.plasma_cannon = defences.plasma_cannon.amount
        Defence.shield_dome_small = defences.shield_dome_small.amount
        Defence.shield_dome_large = defences.shield_dome_large.amount
        Defence.missile_interceptor = defences.missile_interceptor.amount
        Defence.missile_interplanetary = defences.missile_interplanetary.amount
        Defence.save()
        celestial.defences = Defence
        celestial.save()
    return redirect('empireView', universum)


def building(request, universum):
    empire = login(request, universum)
    ids = empire.planet_ids()
    for i, id in enumerate(ids):
        celestial, new = Celestial.objects.get_or_create(
            user=request.user,
            universum=universum,
            coordintate=str(empire.celestial_coordinates(id)),
            name=(empire.planet_names() + empire.moon_names())[i]
        )
        if celestial.buildings_id is not None:
            Building = Buildings(pk=celestial.buildings.id)
        else:
            Building = Buildings()
        supply = empire.supply(id)
        Building.metal_mine = supply.metal_mine.level
        Building.crystal_mine = supply.crystal_mine.level
        Building.deuterium_mine = supply.deuterium_mine.level
        Building.solar_plant = supply.solar_plant.level
        Building.fusion_plant = supply.fusion_plant.level
        Building.metal_storage = supply.metal_storage.level
        Building.crystal_storage = supply.crystal_storage.level
        Building.deuterium_storage = supply.deuterium_storage.level

        facilities = empire.facilities(id)
        Building.robotics_factory = facilities.robotics_factory.level
        Building.shipyard = facilities.shipyard.level
        Building.research_laboratory = facilities.research_laboratory.level
        Building.alliance_depot = facilities.alliance_depot.level
        Building.missile_silo = facilities.missile_silo.level
        Building.nanite_factory = facilities.nanite_factory.level
        Building.terraformer = facilities.terraformer.level
        Building.repair_dock = facilities.repair_dock.level

        Building.save()
        celestial.buildings = Building
        celestial.save()
    return redirect('empireView', universum)
