import folium
import geopy
import openrouteservice as ors
from django.shortcuts import render, redirect
from geopy.distance import geodesic
from .forms import GetLocations
from .utils import arrange_map, get_zoom, get_lat_lng
import math
import json
import requests
from sys import maxsize
from monument.models import Monument
from django.http import HttpResponseRedirect, HttpResponse

# Create your views here.
v = 4


def TSP(graph, s):
    pathx = []
    for i in range(v):
        if i != s:
            pathx.append(i)

    min_path = maxsize
    while True:
        current_distance = 0
        k = s
        for i in range(len(pathx)):
            current_distance += graph[k][pathx[i]]
            k = pathx[i]
        current_distance += graph[k][s]
        min_path = min(min_path, current_distance)

        if not next_perm(pathx):
            break
    return min_path, pathx


def next_perm(p):
    n = len(p)
    i = n - 2

    while i >= 0 and p[i] > p[i + 1]:
        i -= 1
    if i == -1:
        return False

    j = i + 1
    while j < n and p[j] > p[i]:
        j += 1

    j -= 1

    p[i], p[j] = p[j], p[i]
    left = i + 1
    right = n - 1

    while left < right:
        p[left], p[right] = p[right], p[left]
        left += 1
        right -= 1
    return True


def home(request):
    user = request.user
    if not user.is_authenticated:
        return redirect("must_authenticate")

    form = GetLocations(request.POST)
    context={}

    # initial folium map
    map = folium.Map(location=[33.436117, -5.221913], zoom_start=7)
    # popup1 = folium.LatLngPopup()
    # map.add_child(popup1)
    map = map._repr_html_()
    context = {"form": form, 'map': map}

    if form.is_valid():
        #on recupère la ville origine du monument selectionné
        location1 = form.cleaned_data["location1"]
        location2 = form.cleaned_data["location2"]
        location3 = form.cleaned_data["location3"]
        location4 = form.cleaned_data["location4"]

        # Recuperer latitude et longitude de la ville de chaque monument
        lat1, lng1 = get_lat_lng(location1)
        lat2, lng2 = get_lat_lng(location2)
        lat3, lng3 = get_lat_lng(location3)
        lat4, lng4 = get_lat_lng(location4)

        d12 = round(geopy.distance.great_circle((lat1, lng1), (lat2, lng2)).km)
        print('1-2  ' + str(d12))
        d13 = round(geopy.distance.great_circle((lat1, lng1), (lat3, lng3)).km)
        print('1-3  ' + str(d13))
        d14 = round(geopy.distance.great_circle((lat1, lng1), (lat4, lng4)).km)
        print('1-4  ' + str(d14))
        d23 = round(geopy.distance.great_circle((lat2, lng2), (lat3, lng3)).km)
        print('2-3  ' + str(d23))
        d24 = round(geopy.distance.great_circle((lat2, lng2), (lat4, lng4)).km)
        print('2-4  ' + str(d24))
        d34 = round(geopy.distance.great_circle((lat3, lng3), (lat4, lng4)).km)
        print('3-4  ' + str(d34))
        graph = [[0, d12, d13, d14], [d12, 0, d23, d24], [d13, d23, 0, d34], [d14, d24, d34, 0]]
        s = 0
        cout, pathx = TSP(graph, s)
        print("cout "+str(cout)+" path :  "+str(pathx))
        ors_key = '5b3ce3597851110001cf6248af2a466a32b44144a1da58e780b7e9d0'
        client = ors.Client(key=ors_key)
        # coordinates = [[o_lon, o_lat], [d_lon, d_lat]]
        coordinates = [[lng1, lat1], [lng2, lat2], [lng3, lat3], [lng4, lat4]]
        path = [[lng1, lat1], coordinates[pathx[0]], coordinates[pathx[1]], coordinates[pathx[2]], [lng1, lat1]]
        route = client.directions(coordinates=path,
                                  preference='shortest',
                                  profile='driving-car',
                                  format='geojson')
        # Arranger la carte
        map = folium.Map(arrange_map(lat1, lng1, lat2, lng2), zoom_start=7)
        coordinates[pathx[0]].reverse()
        coordinates[pathx[1]].reverse()
        coordinates[pathx[2]].reverse()
        folium.Marker([lat1, lng1], popup='1', icon=folium.Icon(color='red')).add_to(map)
        folium.Marker(coordinates[pathx[0]], popup='2', icon=folium.Icon(color='red')).add_to(map)
        folium.Marker(coordinates[pathx[1]], popup='3', icon=folium.Icon(color='red')).add_to(map)
        folium.Marker(coordinates[pathx[2]], popup='4', icon=folium.Icon(color='red')).add_to(map)
        folium.GeoJson(route, name='route').add_to(map)
        folium.LayerControl().add_to(map)
        # popup1 = folium.LatLngPopup()
        # map.add_child(popup1)
        map = map._repr_html_()

        context = {"form": form, 'lc1': location1, 'lc2': location2, 'lc3': location3, 'map': map}

    trying = Monument.objects.all()
    context['trying'] = trying

    return render(request, 'routing/map.html', context)
