from django.shortcuts import render, redirect, get_object_or_404
from django.core.files import File
import os, qrcode
from django.http import HttpResponse
from django.conf import settings
from authentication.models import Coordinator
from django.http import HttpResponseRedirect
from django.urls import reverse

def coordinator(request):
    return render(request, 'coordinators.html')

def generate_and_save_qr(request):    
    if request.method == 'POST':
        activity = request.POST.get('activity')
        
        coordinator = get_object_or_404(Coordinator, user=request.user)
        
        coordinator.activity = activity
        coordinator.save()
        
        prn = coordinator.prn
        if not prn:
            return HttpResponse("PRN not found", status=400)
        
        # Create the QR code using the simpler method
        qr = qrcode.QRCode(
            version=5,
            box_size=10,
            border=5
        )

        # Include PRN and Activity in the QR code data
        data = f"PRN: {prn}\nActivity: {coordinator.activity}"
        qr.add_data(data)
        qr.make(fit=True)

        # Create an image from the QR code instance
        img = qr.make_image(fill="black", back_color="white")

        # Create the filename and path
        filename = f"{prn}_{activity}.png"  # Using PNG format for better quality
        qr_codes_dir = os.path.join(settings.STATIC_URL, 'qr_codes')

        # Ensure the directory exists
        if not os.path.exists(qr_codes_dir):
            os.makedirs(qr_codes_dir)

        filepath = os.path.join(qr_codes_dir, filename)
        
        # Save the QR code image
        img.save(filepath)

        # Open and save the image in the Coordinator model
        with open(filepath, 'rb') as img_file:
            coordinator.qr_code.save(filename, File(img_file), save=True)

    return render(request, 'coordinators.html', {'coordinator': coordinator})