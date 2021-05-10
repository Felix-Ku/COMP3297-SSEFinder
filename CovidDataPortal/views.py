from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic.list import ListView

from .forms import CaseInputForm
from .forms import AttInputForm
from .forms import InputForm
from django.shortcuts import render

# Import models
from .models import case_records
from .models import attendances
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout # 匯入logout函式

import json
import requests
import urllib.parse
import pandas as pd
import datetime
from datetime import timedelta
from django.shortcuts import render
import pandas as pd
import json

####################### New views.
# @login_required
# def home(request):
#     return render(request, 'home.html', {'username': request.user.username})

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))

def Create_record(request):

    cases = case_records.objects.all()

    form = CaseInputForm()

    if request.method == "POST":
        form = CaseInputForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(All_cases_success)
        else:
            return redirect(Fail_create_cases)
    context = {
        'cases': cases,
        'form': form

    }

    return render(request, 'Create_record.html', context)

def Fail_create_cases(request):

    context = {
    }
    return render(request, 'Fail_create_cases.html', context)

    # context = {
    # }
    # return render(request, 'Create_record.html', context=context)

# Backup class (not working)
# def Create_record(request):
#
#     # context = {
#     # }
#     # return render(request, 'Create_record.html', context=context)
#
#     if request.method == "POST":
#         form = CaseInputForm(request.POST)
#         if form.is_valid():
#             case_number = request.POST.get('case_number','')
#             person_name = request.POST.get('person_name', '')
#             id_number = request.POST.get('id_number', '')
#             birth_date = request.POST.get('birth_date', '')
#             symptoms_date = request.POST.get('symptoms_date', '')
#             confirmation_date = request.POST.get('confirmation_date', '')
#             cases_obj = cases(case_number=case_number, person_name=person_name, id_number=id_number,birth_date=birth_date, symptoms_date=symptoms_date, confirmation_date=confirmation_date)
#             cases_obj.save()
#
#             # Add notice telling user of successful input
#             return HttpResponseRedirect(reverse(All_cases)) # Jump to page after input of information
#     else:
#         form = CaseInputForm()
#
#     return render(request, 'Create_record.html', {
#             'form': form,
#         })

def Case_query(request):


    if 'q' in request.GET and request.GET['q']:
        q = request.GET['q']
        cases = case_records.objects.all().filter(case_number=q)
        message = "Case number searched: "+q
        if len(cases) == 0:
            status = "Case not found!"
        else:
            status = "Case found!"
    else:
        cases = case_records.objects.all()
        message = "Showing all cases"
        status = "Awaiting search action..."

    return render(request, 'Case_query.html', {'cases': cases, 'message': message, 'status':status})



def Attendance_query(request):

    if 'q' in request.GET and request.GET['q']:
        q = request.GET['q']
        attendance = attendances.objects.all().filter(case_number_link=q)
        message = str(q)
        if len(attendance) == 0:
            status = "Attendance records not found!"
        else:
            status = "Attendance records found!"
    else:
        attendance = attendances.objects.all()
        message = "ALL"
        status = "Awaiting search action..."

    return render(request, 'Attendance_query.html', {'attendance': attendance, 'message': message, 'status': status})

    # target_case = ""
    # found = ""
    # cases = case_records.objects.all()
    #
    # if request.method == "POST":
    #     found = False
    #     selected_case = request.POST.get("case_number")
    #     for case in cases:
    #         if case.case_number == selected_case:
    #             target_case = case
    #             found = True
    #             break
    #
    # ### Extract data of location
    # if found == False:
    #     message = "Case not found!"
    # elif found == True:
    #     message = "Case found!"
    # else:
    #     message = "Awaiting action"
    #
    # context = {
    #     'target_case': target_case,
    #     'message': message,
    #     'cases': cases
    # }
    #
    # return render(request, 'Case_query.html', context=context)


def Create_attendance(request):
    if 'q' in request.GET and request.GET['q']:
        # If yes search action
        q = request.GET['q']
        case = case_records.objects.all().filter(case_number=q)

        if len(case) == 0:
            status = "Case not found!"
            Selected = "None"
            cases = ""
        elif len(case) == 1:
            status = "Case found!"
            Selected = str(q)
            cases = case
        elif len(case) >1:
            status = "Cases with duplicate number found, please check your database."
            Selected = "None"
            cases = ""

    else: # If no search action
        Selected = "None"
        status = "Awaiting search action, please input a search."
        cases = ""

    if cases!="":
        form = AttInputForm(initial={'address': "LEAVE BLANK for AUTO-INPUT",'hk_grid': "LEAVE BLANK for AUTO-INPUT",'case_number_link': cases.first()})
    else:
        form = AttInputForm(initial={'address': "LEAVE BLANK for AUTO-INPUT", 'hk_grid': "LEAVE BLANK for AUTO-INPUT",
                                     'case_number_link':'CASE NOT SELECTED!'})

    if request.method == "POST":
        form = AttInputForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            venue_name = form.data.get('venue_name', None)
            event_date = form.data.get('event_date', None)
            if venue_name is not None:
                link = "https://geodata.gov.hk/gs/api/v1.0.0/locationSearch?q="
                link += urllib.parse.quote(str(venue_name))
                try:
                    resp = requests.get(url=link)
                    data = resp.json()
                    df = pd.DataFrame(data)
                    if cases != "":
                        date_symptom = datetime.datetime.strptime(str(cases[0].symptoms_date), '%d-%m-%Y')
                        date_confirm = datetime.datetime.strptime(str(cases[0].confirmation_date), '%d-%m-%Y')
                        date_event = datetime.datetime.strptime(str(event_date), '%d-%m-%Y')
                        days14 = date_symptom - timedelta(days=14)
                        if not (days14 <= date_event <= date_confirm):
                            return redirect(Fail_date)
                    else:
                        return redirect(Fail_create)
                except:
                    data_status = "Unsuccessful"
                    return redirect(Fail_create)
                if df.empty:
                    data_status = "Unsuccessful"
                    add = "Unsuccessful retrieval"
                    grid = "Unsuccessful retrieval"
                else:
                    data_status = "Successful"
                    x = df.iloc[0]["x"]
                    y = df.iloc[0]["y"]
                    grid = str(x) + "," + str(y)
                    add = str(df.iloc[0]["addressEN"])
            instance.hk_grid = grid
            instance.address = add
            instance.save()
        return redirect(All_cases_success)

    context = {
        'cases': cases,
        'form': form,
        'Selected': Selected,
        'status': status
    }

    # form.cleaned_data['Email'] = GetEmailString()
    # id = form.cleaned_data.get('id', None)
    # cleaned_data / data
    # date_symptom=datetime.datetime.strptime(date_time_str, '%d/%m/%Y')
    # date_confirm=datetime.datetime.strptime(date_time_str, '%d/%m/%Y')
    # date_event=datetime.datetime.strptime(date_time_str, '%d/%m/%Y')

    return render(request, 'Create_attendance.html', {'form':form, 'cases': cases, 'Selected': Selected, 'status': status})

def All_cases(request):

    cases = case_records.objects.all()

    context = {
        'cases': cases
    }
    return render(request, 'All_cases.html', context=context)

def Fail_date(request):

    context = {
    }
    return render(request, 'Fail_date.html', context=context)

def Fail_create(request):

    context = {
    }
    return render(request, 'Fail_create.html', context=context)

def All_cases_success(request):

    cases = case_records.objects.all()

    context = {
        'cases': cases
    }
    return render(request, 'All_cases_success.html', context=context)

def SSE_Finder(request):

    cases_all = case_records.objects.all().values()
    events_all = attendances.objects.all().values()
    events = attendances.objects.all()

    df = pd.DataFrame(events_all)

    groupdf = df.groupby(['venue_name', 'venue_location']).size().to_frame('count').reset_index()
    df2 = groupdf[groupdf["count"] >= 6]



    # list_count = []
    # list_venue_name = []
    # list_venue_location = []
    list_venue_name = df2['venue_name'].values.tolist()
    list_address = []
    list_hk_grid = []
    list_event_date = []
    list_description = []

    for venue in list_venue_name:
        for event in events:
            if (str(event.venue_name)==str(venue)):
                list_address.append(str(event.address))
                list_hk_grid.append(str(event.hk_grid))
                list_event_date.append(str(event.event_date))
                list_description.append(str(event.description))
                break

    df2["address"] = list_address
    df2["hk_grid"] = list_hk_grid
    df2["event_date"] = list_event_date
    df2["description"] = list_description
    # print(list_address)
    # print(list_hk_grid)
    # print(list_event_date)
    # print(list_description)


    print(df2)

    # list_count = df2['count'].values.tolist()
    # list_venue_name = df2['venue_name'].values.tolist()
    # list_venue_location = df2['venue_location'].values.tolist()
    # list_address = df2['address'].values.tolist()
    # list_hk_grid = df2['hk_grid'].values.tolist()
    # list_event_date = df2['event_date'].values.tolist()
    # list_description = df2['description'].values.tolist()

    json_records = df2.reset_index().to_json(orient='records')
    data = []
    data = json.loads(json_records)

    if request.method == "POST":
        form = InputForm(request.POST)
        if form.is_valid():

            from_date = request.POST.get('from_date', '')
            to_date = request.POST.get('to_date', '')
            from_date_t = datetime.datetime.strptime(from_date, '%d-%m-%Y')
            to_date_t = datetime.datetime.strptime(to_date, '%d-%m-%Y')

            date = str(from_date)+"-"+str(to_date)

            df2['event_date'] = pd.to_datetime(df2['event_date'], format='%d-%m-%Y')
            df3 = df2[df2['event_date'] <= to_date_t]
            print(df3)
            df4 = df3[from_date_t <= df3['event_date']]
            print(df4)
            json_records = df4.reset_index().to_json(orient='records')
            dataS = []
            dataS = json.loads(json_records)
            context = {'Selected':date, 'status': "Successful", 'd': data, 'form': form, 's': dataS}
        else:
            context = {'Selected': "", 'status': "Unsuccessful", 'd': data, 'form': form, 's':''}

    else:
        form = InputForm()
        context = {'Selected': "", 'status': "Unsuccessful", 'd': data, 'form': form, 's':''}

    return render(request, 'SSE_Finder.html', context)
    # return render(request, 'SSE_Finder.html', {
    #     'form': form,
    # })

def SSE_query(request):

    case = "ABC"
    if 'q' in request.GET and request.GET['q']:
        q = request.GET['q']

        case = str(q)

        # cases = case_records.objects.all().filter(case_number=q)
        # if len(cases) == 0:
        #     status = "Case not found!"
        # else:
        #     status = "Case found!"
    # else:
        # cases = case_records.objects.all()
        # message = "Showing all cases"
        # status = "Awaiting search action..."

    return render(request, 'SSE_query.html', {'case': case, 'Selected': "Selected" })

def index(request):
    context = {
    }
    return render(request, 'index.html', context=context)

def login(request):
    context = {
    }
    return render(request, 'registration/login.html', context=context)

    # ## Select form location
    # locations = Location_data.objects.filter()
    # form = request.POST
    # selected_region = "Hong Kong"  # Default location as Hong Kong
    # data_status = "Waiting for action"
    #
    # if request.method == "POST":
    #     selected_region = request.POST.get("location")
    #
    # ### Extract data of location
    # found = False
    # locations = Location_data.objects.filter()
    # for location in locations:
    #     if location.name == selected_region:
    #         location_pop = location.Pop
    #         location_name = location.name
    #         location_api = location.api
    #         location_url = location.url
    #         found = True
    #         break
    #
    # if (found==False):
    #     selected_region = "NONE"
    #     location_date = location_pop = location_name = location_confirmed_total = location_confirmed_total_perMil = location_fatalities_total = location_fatalities_total_perMil = location_new = location_new_WeekAvg = location_fatalities_new = location_fatalities_new_WeekAvg = "NO DATA"
    #
    # else:
    #     datelist = []
    #     for num in range(0, 9):
    #         datelist.append((datetime.datetime.today() - datetime.timedelta(days=num)).strftime('%d/%m/%Y'))
    #
        # link = location_api
        #
        # q = {
        #     "resource": location_url,
        #     "section": 1,
        #     "format": "json",
        #     "filters": [[1, "in", datelist]]
        # }
        #
        # j = json.dumps(q)
        # query_str = urllib.parse.quote(j)
        # link += "?q=" + query_str
        #
        # data_status = "Successful"
        #
        # try:
        #     resp = requests.get(url=link)
        #     data = resp.json()
        #     df = pd.DataFrame(data)
        # except:
        #     data_status = "Unsuccessful"
        #
        # if data_status == "Successful":
        #     df["new_case"] = df["Number of confirmed cases"].shift(-1) - df["Number of confirmed cases"]
        #     df["new_fatal"] = df["Number of death cases"].shift(-1) - df["Number of death cases"]
        #
        #     location_date = df["As of date"].iloc[-1]
        #     location_confirmed_total = df["Number of confirmed cases"].iloc[-1]
        #     location_confirmed_total_perMil = round(location_confirmed_total / (location_pop / 1000000), 2)
        #     location_fatalities_total = df["Number of death cases"].iloc[-1]
        #     location_fatalities_total_perMil = round(location_fatalities_total / (location_pop / 1000000), 2)
        #
        #     location_new = df["new_case"].iloc[-2]
        #     location_new_WeekAvg = round(df["new_case"].iloc[-8:-1].mean(), 2)
        #
        #     location_fatalities_new = df["new_fatal"].iloc[-2]
        #     location_fatalities_new_WeekAvg = round(df["new_fatal"].iloc[-8:-1].mean(), 2)
        # else:
        #     location_date = location_confirmed_total = location_confirmed_total_perMil = location_fatalities_total = location_fatalities_total_perMil = location_new = location_new_WeekAvg = location_fatalities_new = location_fatalities_new_WeekAvg = "NO DATA"
        #     data_status = "Unsuccessful - Check API or URL links"
    #
    #
    # context = {
    #     'locations': locations,
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
    #     'data_status': data_status,
    #     'selected_region': selected_region
    # }

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



####################### Old views.

# def AddLocation(request):
#     # context = {
#     # }
#     # return render(request, 'AddLocation.html', context=context)
#     if request.method == "POST":
#         form = InputForm(request.POST)
#         if form.is_valid():
#             location = request.POST.get('location','')
#             Pop = request.POST.get('Pop', '')
#             api = request.POST.get('api', '')
#             url = request.POST.get('url', '')
#             location_obj = Location_data(name=location, Pop=Pop, url=url,api=api)
#             location_obj.save()
#
#             return HttpResponseRedirect(reverse(LocationData_list_view))
#     else:
#         form = InputForm()
#
#     return render(request, 'AddLocation.html', {
#             'form': form,
#         })
#
# def SelectLocation(request):
#     context = {
#     }
#     return render(request, 'SelectLocation.html', context=context)
#
# def LocationData_list_view(request):
#     queryset = Location_data.objects.all()
#     context = {
#         "object_list": queryset
#     }
#     return render(request, 'LocationData_list.html', context=context)
