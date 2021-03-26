from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic.list import ListView

from .forms import InputForm
from .forms import dateform
from .models import Location_data
import json
import requests
import urllib.parse
import pandas as pd
import datetime


# Create your views here.
def index(request):

    ## Select form location
    locations = Location_data.objects.filter()
    form = request.POST
    selected_region = "Hong Kong"  # Default location as Hong Kong
    data_status = "Waiting for action"

    if request.method == "POST":
        selected_region = request.POST.get("location")

    ### Extract data of location
    found = False
    locations = Location_data.objects.filter()
    for location in locations:
        if location.name == selected_region:
            location_pop = location.Pop
            location_name = location.name
            location_api = location.api
            location_url = location.url
            found = True
            break

    if (found==False):
        selected_region = ""
        location_date = location_pop = location_name = location_confirmed_total = location_confirmed_total_perMil = location_fatalities_total = location_fatalities_total_perMil = location_new = location_new_WeekAvg = location_fatalities_new = location_fatalities_new_WeekAvg = "NO DATA"

    else:
        datelist = []
        for num in range(0, 9):
            datelist.append((datetime.datetime.today() - datetime.timedelta(days=num)).strftime('%d/%m/%Y'))

        link = location_api

        q = {
            "resource": location_url,
            "section": 1,
            "format": "json",
            "filters": [[1, "in", datelist]]
        }

        j = json.dumps(q)
        query_str = urllib.parse.quote(j)
        link += "?q=" + query_str

        data_status = "Successful"

        try:
            resp = requests.get(url=link)
            data = resp.json()
            df = pd.DataFrame(data)
        except:
            data_status = "Unsuccessful"

        if data_status == "Successful":
            df["new_case"] = df["Number of confirmed cases"].shift(-1) - df["Number of confirmed cases"]
            df["new_fatal"] = df["Number of death cases"].shift(-1) - df["Number of death cases"]

            location_date = df["As of date"].iloc[-1]
            location_confirmed_total = df["Number of confirmed cases"].iloc[-1]
            location_confirmed_total_perMil = round(location_confirmed_total / (location_pop / 1000000), 2)
            location_fatalities_total = df["Number of death cases"].iloc[-1]
            location_fatalities_total_perMil = round(location_fatalities_total / (location_pop / 1000000), 2)

            location_new = df["new_case"].iloc[-2]
            location_new_WeekAvg = round(df["new_case"].iloc[-8:-1].mean(), 2)

            location_fatalities_new = df["new_fatal"].iloc[-2]
            location_fatalities_new_WeekAvg = round(df["new_fatal"].iloc[-8:-1].mean(), 2)
        else:
            location_date = location_confirmed_total = location_confirmed_total_perMil = location_fatalities_total = location_fatalities_total_perMil = location_new = location_new_WeekAvg = location_fatalities_new = location_fatalities_new_WeekAvg = "FAILED TO RETRIEVED"


    context = {
        'locations': locations,
        'location_pop': location_pop,
        'location_name': location_name,
        'location_date': location_date,
        'location_confirmed_total': location_confirmed_total,
        'location_confirmed_total_perMil': location_confirmed_total_perMil,
        'location_fatalities_total': location_fatalities_total,
        'location_fatalities_total_perMil': location_fatalities_total_perMil,
        'location_new': location_new,
        'location_new_WeekAvg': location_new_WeekAvg,
        'location_fatalities_new': location_fatalities_new,
        'location_fatalities_new_WeekAvg': location_fatalities_new_WeekAvg,
        'data_status': data_status,
        'selected_region': selected_region
    }

    ## Method 2 - Direct process csv
    # locations = Location_data.objects.filter()
    # for location in locations:
    #     if location.name == "Hong Kong":
    #         location_pop = location.Pop
    #         location_name = location.name
    #         location_api = location.api
    #
    # data_status = "Successful"
    #
    # try:
    #     response = requests.get('http://www.chp.gov.hk/files/misc/latest_situation_of_reported_cases_covid_19_eng.csv')
    #     file_object = io.StringIO(response.content.decode('utf-8'))
    #     df_HongKong = pd.read_csv(file_object)
    # except:
    #     data_status = "Unsuccessful"
    #
    # if data_status == "Successful":
    #     df_HongKong["confirmed_new"] = df_HongKong["Number of confirmed cases"].shift(-1)-df_HongKong["Number of confirmed cases"]
    #     df_HongKong["fatalities_new"] = df_HongKong["Number of death cases"].shift(-1)-df_HongKong["Number of death cases"]
    #
    #     location_date = df_HongKong["As of date"].iloc[-1]
    #     location_confirmed_total = df_HongKong["Number of confirmed cases"].iloc[-1]
    #     location_confirmed_total_perMil = round(location_confirmed_total/(location_pop/1000000),2)
    #     location_fatalities_total = df_HongKong["Number of death cases"].iloc[-1]
    #     location_fatalities_total_perMil = round(location_fatalities_total/(location_pop/1000000),2)
    #
    #     location_new = df_HongKong["confirmed_new"].iloc[-2]
    #     location_new_WeekAvg = round(df_HongKong["confirmed_new"].iloc[-8:-1].mean(),2)
    #
    #     location_fatalities_new = df_HongKong["fatalities_new"].iloc[-2]
    #     location_fatalities_new_WeekAvg = round(df_HongKong["fatalities_new"].iloc[-8:-1].mean(),2)
    # else:
    #     location_date = location_confirmed_total = location_confirmed_total_perMil = location_fatalities_total = location_fatalities_total_perMil = location_new = location_new_WeekAvg = location_fatalities_new = location_fatalities_new_WeekAvg = "NO DATA"
    #
    # context = {
    #     'location_pop': location_pop,
    #     'location_name': location_name,
    #     'location_date': location_date,
    #     'location_confirmed_total': location_confirmed_total,
    #     'location_confirmed_total_perMil': location_confirmed_total_perMil,
    #     'location_fatalities_total': location_fatalities_total,
    #     'location_fatalities_total_perMil': location_fatalities_total_perMil,
    #     'location_new': location_new,
    #     'location_new_WeekAvg': location_new_WeekAvg,
    #     'location_fatalities_new': location_fatalities_new,
    #     'location_fatalities_new_WeekAvg': location_fatalities_new_WeekAvg,
    #     'data_status' : data_status,
    # }

    return render(request, 'index.html', context=context)


# Create your views here.
def AddLocation(request):
    # context = {
    # }
    # return render(request, 'AddLocation.html', context=context)
    if request.method == "POST":
        form = InputForm(request.POST)
        if form.is_valid():
            location = request.POST.get('location','')
            Pop = request.POST.get('Pop', '')
            api = request.POST.get('api', '')
            url = request.POST.get('url', '')
            location_obj = Location_data(name=location, Pop=Pop, url=url,api=api)
            location_obj.save()

            return HttpResponseRedirect(reverse(LocationData_list_view))
    else:
        form = InputForm()

    return render(request, 'AddLocation.html', {
            'form': form,
        })


# Create your views here.
def SelectLocation(request):
    context = {
    }
    return render(request, 'SelectLocation.html', context=context)

def LocationData_list_view(request):
    queryset = Location_data.objects.all()
    context = {
        "object_list": queryset
    }
    return render(request, 'LocationData_list.html', context=context)

# Create your views here.
def index_test(request):

    ## Select form location
    locations = Location_data.objects.filter()
    form = request.POST
    selected_region = None
    selected_region = "Hong Kong"  # Default location as Hong Kong
    if request.method == "POST":
        selected_region = request.POST.get("location")

    ### Extract data of location
    found = False
    locations = Location_data.objects.filter()
    for location in locations:
        if location.name == selected_region:
            location_pop = location.Pop
            location_name = location.name
            location_api = location.api
            location_url = location.url
            found = True
            break

    datelist = []
    for num in range(0, 9):
        datelist.append((datetime.datetime.today() - datetime.timedelta(days=num)).strftime('%d/%m/%Y'))

    if (found == True):
        link = location_api

        q = {
            "resource": location_url,
            "section": 1,
            "format": "json",
            "filters": [[1, "in", datelist]]
        }

        j = json.dumps(q)
        query_str = urllib.parse.quote(j)
        link += "?q=" + query_str

        data_status = "Successful"

        try:
            resp = requests.get(url=link)
            data = resp.json()
            df = pd.DataFrame(data)
        except:
            data_status = "Unsuccessful"

        if data_status == "Successful":
            df["new_case"] = df["Number of confirmed cases"].shift(-1) - df["Number of confirmed cases"]
            df["new_fatal"] = df["Number of death cases"].shift(-1) - df["Number of death cases"]

            location_date = df["As of date"].iloc[-1]
            location_confirmed_total = df["Number of confirmed cases"].iloc[-1]
            location_confirmed_total_perMil = round(location_confirmed_total / (location_pop / 1000000), 2)
            location_fatalities_total = df["Number of death cases"].iloc[-1]
            location_fatalities_total_perMil = round(location_fatalities_total / (location_pop / 1000000), 2)

            location_new = df["new_case"].iloc[-2]
            location_new_WeekAvg = round(df["new_case"].iloc[-8:-1].mean(), 2)

            location_fatalities_new = df["new_fatal"].iloc[-2]
            location_fatalities_new_WeekAvg = round(df["new_fatal"].iloc[-8:-1].mean(), 2)
        else:
            location_date = location_confirmed_total = location_confirmed_total_perMil = location_fatalities_total = location_fatalities_total_perMil = location_new = location_new_WeekAvg = location_fatalities_new = location_fatalities_new_WeekAvg = "NO DATA"
    else:
        location_date = location_confirmed_total = location_confirmed_total_perMil = location_fatalities_total = location_fatalities_total_perMil = location_new = location_new_WeekAvg = location_fatalities_new = location_fatalities_new_WeekAvg = "NO DATA"
        data_status = "Unsuccessful"

    form_date = dateform(request.POST)

    context = {
        'locations': locations,
        'location_pop': location_pop,
        'location_name': location_name,
        'location_date': location_date,
        'location_confirmed_total': location_confirmed_total,
        'location_confirmed_total_perMil': location_confirmed_total_perMil,
        'location_fatalities_total': location_fatalities_total,
        'location_fatalities_total_perMil': location_fatalities_total_perMil,
        'location_new': location_new,
        'location_new_WeekAvg': location_new_WeekAvg,
        'location_fatalities_new': location_fatalities_new,
        'location_fatalities_new_WeekAvg': location_fatalities_new_WeekAvg,
        'data_status': data_status,
        'selected_region': selected_region,
        'dateform': form_date
    }

    return render(request, 'index_test.html', context=context)
