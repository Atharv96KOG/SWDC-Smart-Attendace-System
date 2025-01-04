from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from authentication.models import Volunteer
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from authentication.models import Attendance, Coordinator
import json

def volunteer(request):
    return render(request, 'volunteers.html')

@login_required
def allot_activity(request):
    if request.method == 'POST':
        activity = request.POST.get('activity')
        volunteer = get_object_or_404(Volunteer, user=request.user)
        volunteer.activity = activity
        volunteer.save()
    else:
        volunteer = get_object_or_404(Volunteer, user=request.user)
    return render(request, 'volunteers.html', {'volunteer': volunteer})


@method_decorator(csrf_exempt, name='dispatch')  
class MarkAttendanceView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        try:
            # Determine if the request is JSON or FormData
            if request.content_type.startswith('application/json'):
                # Handle JSON data (e.g., from QR scanner)
                data = json.loads(request.body)
                coord_prn = data.get('coord_prn')
                activity = data.get('activity')
                
                if not coord_prn or not activity:
                    return JsonResponse({'error': 'Missing coord_prn or activity.'}, status=400)
                
                # Create Attendance record
                attendance = Attendance.objects.create(
                    coordinator_prn=coord_prn,
                    activity=activity,
                    volunteer=request.user,  # Assuming the user is authenticated
                )
                
                return JsonResponse({'message': 'Attendance marked successfully!'}, status=200)
            
            elif 'geo_photo' in request.FILES:
                # Handle FormData (e.g., from photo capture)
                coord_name = request.POST.get('coord_name')
                coord_prn = request.POST.get('coord_prn')
                vol_name = request.POST.get('vol_name')
                vol_prn = request.POST.get('vol_prn')
                actual_latitude = request.POST.get('actual_latitude')
                actual_longitude = request.POST.get('actual_longitude')
                geo_photo = request.FILES.get('geo_photo')
                activity = request.POST.get('activity')  # Ensure 'activity' is included in the form
                
                if not all([coord_prn, vol_name, vol_prn, actual_latitude, actual_longitude, geo_photo, activity]):
                    return JsonResponse({'error': 'Incomplete attendance data.'}, status=400)
                
                # Create Attendance record with photo
                attendance = Attendance.objects.create(
                    coordinator_prn=coord_prn,
                    activity=activity,
                    volunteer=request.user,
                    latitude=actual_latitude,
                    longitude=actual_longitude,
                    photo=geo_photo,
                )
                
                return JsonResponse({'message': 'Attendance with photo marked successfully!'}, status=200)
            
            else:
                return JsonResponse({'error': 'Unsupported Content-Type.'}, status=400)
        
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON.'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    def get(self, request, *args, **kwargs):
        return JsonResponse({'error': 'GET method not allowed.'}, status=405)