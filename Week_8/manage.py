# Install required packages
!pip install django tensorflow pyngrok

# Create Django project structure
!django-admin startproject shoplifting_detector
%cd shoplifting_detector
!python manage.py startapp detector

# Write minimal Django files
%%writefile detector/views.py
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from tensorflow.keras.models import load_model
import cv2
import numpy as np
import os

model = load_model('shoplifting_detector.h5')  # Make sure to upload your model first

def predict_video(video_path):
    # Your prediction logic here (simplified example)
    return "Shoplifter" if np.random.rand() > 0.5 else "Non-Shoplifter"

def upload_file(request):
    if request.method == 'POST' and request.FILES['video']:
        video = request.FILES['video']
        fs = FileSystemStorage()
        filename = fs.save(video.name, video)
        result = predict_video(fs.path(filename))
        return HttpResponse(f"Prediction: {result}")
    return HttpResponse('''
        <form method="post" enctype="multipart/form-data">
          <input type="file" name="video">
          <button type="submit">Upload</button>
        </form>
    ''')

%%writefile shoplifting_detector/urls.py
from django.contrib import admin
from django.urls import path
from detector.views import upload_file

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', upload_file),
]

# Update settings
%%writefile shoplifting_detector/settings.py
import os

SECRET_KEY = 'django-insecure-test-key'
DEBUG = True
ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'detector',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'shoplifting_detector.urls'
STATIC_URL = 'static/'
MEDIA_URL = 'media/'
MEDIA_ROOT = os.path.join(os.getcwd(), 'media')
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Create media directory
!mkdir media

# Migrate database
!python manage.py migrate

# Run Django server with ngrok
from pyngrok import ngrok
import threading
import time
import subprocess

def run_django():
    subprocess.call(['python', 'manage.py', 'runserver', '0.0.0.0:8000'])

thread = threading.Thread(target=run_django)
thread.daemon = True
thread.start()

time.sleep(3)  # Wait for server to start
public_url = ngrok.connect(8000)
print("Your Django app is available at:", public_url)