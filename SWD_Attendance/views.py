from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from authentication.models import Volunteer, Coordinator, Secretary

def home(request):
    return render(request, 'main.html')

def update(request):
    return render(request, 'update.html')

def logout_view(request):
    logout(request)
    return redirect('userlogin')

@login_required
def profile(request):
    user = request.user  # Get the logged-in user
    # Get the role-specific profile (Volunteer, Coordinator, Secretary)
    role_info = None
    if hasattr(user, 'volunteer'):
        role_info = user.volunteer
    elif hasattr(user, 'coordinator'):
        role_info = user.coordinator
    elif hasattr(user, 'secretary'):
        role_info = user.secretary

    context = {
        'user': user,
        'role_info': role_info,
    }
    return render(request, 'profile.html', context)

@login_required
def update_profile(request):
    user = request.user 
    role_info = None
    if hasattr(user, 'volunteer'):
        role_info = user.volunteer
    elif hasattr(user, 'coordinator'):
        role_info = user.coordinator
    elif hasattr(user, 'secretary'):
        role_info = user.secretary
        
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        old_pass = request.POST.get('old_pass')
        new_pass = request.POST.get('new_pass')
        c_pass = request.POST.get('c_pass')
        profile_pic = request.FILES.get('profile_pic')

        # Check the old password every time
        if user.check_password(old_pass):
            user.username = name
            user.email = email
            
            # Check for new password only if provided
            if new_pass:
                if new_pass == c_pass:
                    user.set_password(new_pass)
                    user.save()
                    update_session_auth_hash(request, user)  # Keep the user logged in
                else:
                    messages.error(request, 'New passwords do not match.')
                    return redirect('update')

            # Handle profile picture update
            if profile_pic:
                if hasattr(user, 'volunteer'):
                    user.volunteer.profile_picture = profile_pic
                    user.volunteer.save()
                elif hasattr(user, 'coordinator'):
                    user.coordinator.profile_picture = profile_pic
                    user.coordinator.save()
                elif hasattr(user, 'secretary'):
                    user.secretary.profile_picture = profile_pic
                    user.secretary.save()

            user.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('update')
        else:
            messages.error(request, 'Old password is incorrect.')

    context = {
        'role_info': role_info,
    }
    return render(request, 'profile.html', context)
