from urllib.parse import urlencode
from django.core.paginator import Paginator, EmptyPage
from django.shortcuts import render_to_response, redirect
from django.urls import reverse

from app.settings import BUS_STATION_CSV
import csv


def url_with_querystring(path, **kwargs):
    return path + '?' + urlencode(kwargs)


def open_file():
    station_list = []
    with open(BUS_STATION_CSV, newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            station_dict = {'Name': row.get('Name'),
                            'Street': row.get('Street'),
                            'District': row.get('District'),
                            }
            station_list.append(station_dict)
    return station_list


def index(request):
    return redirect(reverse(bus_stations))


def bus_stations(request):
    current_page = int(request.GET.get('page', 1))
    by_page = 10
    paginator = Paginator(open_file(), by_page)
    page_obj = paginator.get_page(current_page)
    if page_obj.has_next():
        page_obj.next_page_number()
    try:
        next_page_url = url_with_querystring(reverse(bus_stations), page=page_obj.next_page_number())
    except EmptyPage:
        next_page_url = None
    if page_obj.has_previous():
        page_obj.previous_page_number()
    try:
        prev_page_url = url_with_querystring(reverse(bus_stations), page=page_obj.previous_page_number())
    except EmptyPage:
        prev_page_url = None
    return render_to_response('index.html', context={
        'bus_stations': page_obj.object_list,
        'current_page': current_page,
        'prev_page_url': prev_page_url,
        'next_page_url': next_page_url,
    })

