from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from authentication.models import Activity
from datetime import datetime


def secretary(request):
    return render(request, 'secretary.html')

def add_activity(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        datetime_str = request.POST.get('datetime')
        map_link = request.POST.get('map_link')
        description = request.POST.get('description')

        # Split datetime into date and time
        if datetime_str:
            date_time_obj = datetime.strptime(datetime_str, "%Y-%m-%dT%H:%M")
            activity_date = date_time_obj.date()
            activity_time = date_time_obj.time()
        else:
            activity_date = None
            activity_time = None

        # Create and save the new Activity object
        new_activity = Activity(
            name=name,
            date=activity_date,
            time=activity_time,
            map_link=map_link,
            description=description,
        )
        new_activity.save()

        return redirect('secretary.html')  

    return render(request, 'secretary.html')  # Render form again if GET method