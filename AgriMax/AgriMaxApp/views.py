# import uuid
import json
import os
from datetime import datetime
import requests
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout  # get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm  # , UserCreationForm
# from django.contrib.auth.models import User
# from django.core.mail import send_mail
from django.http import (HttpResponse, HttpResponseBadRequest,
                         HttpResponseForbidden, HttpResponseRedirect,
                         JsonResponse, StreamingHttpResponse)
from django.shortcuts import redirect, render
from django.urls import reverse
from django_ratelimit.decorators import ratelimit

from .forms import (CustomRegistrationForm, FarmDataForm, HealthDataForm,
                    LocationForm)
from .get_coordinates import get_latitude_longitude
from .health import Health
from .models import CustomUser, Profile

# from .forms import CustomRegistrationForm

# Create your views here.


def get_loginPage(request):
    return render(request, "login.html")


def get_signupPage(request):
    return render(request, "signup.html")


def get_weatherPage(request):
    # Replace with your OpenWeatherMap API key

    json_file = "/home/skye/skye@fieldmanagement/weather_data_2024-09-28_17-05-15.json"
    with open(json_file, 'r') as json_file:
        weather_data = json_file.read()
    # Parse the JSON data
    data = json.loads(weather_data)

    # Extract relevant weather information
    context = {
        "location": data.get("name"),
        "country": data["sys"].get("country"),
        # Convert from Kelvin to Celsius
        "temperature": data["main"].get("temp") - 273.15,
        "icon": data["weather"][0].get("icon"),
        # Convert from Kelvin to Celsius
        "visibility": data['visibility'],
        "feels_like": data["main"].get("feels_like") - 273.15,
        "humidity": data["main"].get("humidity"),
        "pressure": data["main"].get("pressure"),
        "wind_speed": data["wind"].get("speed"),
        "wind_direction": data["wind"].get("deg"),
        "weather_main": data["weather"][0].get("main"),
        "weather_description": data["weather"][0].get("description"),
        # Default to 0 if no rain data
        "rain_last_hour": data.get("rain", {}).get("1h", 0),
        "cloud_cover": data["clouds"].get("all"),
        "sunrise": datetime.fromtimestamp(data["sys"].get("sunrise")).strftime("%H:%M:%S"),  # Convert epotch time to readable time
        "sunset": datetime.fromtimestamp(data["sys"].get("sunset")).strftime("%H:%M:%S"),
    }

    return render(request, 'weather.html', context)
    '''else:
        return render(request, 'weather.html')  '''


def get_historyPage(request):
    return render(request, "history.html")


@login_required
def get_homePage_rec(request):
    recommendations = request.session.get('recommendations', {})
    # Clear the recommendations from the session if you don't need it anymore
    if 'recommendations' in request.session:
        del request.session['recommendations']
    return render(request, "index.html", {'recommendations': recommendations})


@login_required
def get_homePage_crop_rec(request):
    crop_rec = request.session.get('crop_rec', {})
    # Clear the recommendations from the session if you don't need it anymore
    if 'crop_rec' in request.session:
        del request.session['crop_rec']
    return render(request, "index.html", {'crop_rec': crop_rec})


@login_required
def get_homePage(request):
    return render(request, "index.html")


# login view
@ratelimit(key='ip', rate='5/m', method='ALL', block=True)
def user_login(request):

    if getattr(request, 'limited', False):
        return HttpResponseForbidden('Rate limit exceeded')

    if request.method == "POST":
        # Instantiate the form with submitted data
        form = AuthenticationForm(request, data=request.POST)

        # Check wether the form is valid
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(
                request, username=cd['username'], password=cd['password'])

            # Check if the user exists
            try:
                user = CustomUser.objects.get(username=cd["username"])
            except CustomUser.DoesNotExist:
                messages.error(request, 'User does not exist.')
                return render(request, 'login.html')

            # User exists
            if user is not None:
                if user.is_active:
                    login(request, user)
                    # messages.success(request, f'Welcome, {cd["username"]}. You are now logged in.')
                    return redirect('home')

                else:
                    messages.error(request, 'Account is disabled❌')
                    # HttpResponse('<script>alert("Account is disabled❌")</script>')

            # User exists
            else:
                messages.error(request, 'Incorrect login credentials')
                # Using <script> tags directly in messages is not a good practice and can introduce security vulnerabilities, such as cross-site scripting (XSS) attacks.
                # HttpResponse('<script>alert("Incorrect credentials")</script>')

        else:
            messages.error(request, 'Invalid username or password.')

    # When the user_login view is submitted via GET request a new login form is Instantiated with for = LoginForm() to display it in the template.
    else:
        # form = LoginForm()
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


# Signup/Register View
def signup(request):
    if request.method == 'POST':
        form = CustomRegistrationForm(request.POST)

        if form.is_valid():

            user = form.save()

            '''# Create a Profile instance for the new user
            profile = Profile.objects.get(user=user)

            # Generate a unique token
            token = str(uuid.uuid4())
            profile.verification_token = token  # Assuming you have a Profile model
            profile.save()

            # Send verification email
            verification_link = request.build_absolute_uri(
                f'/verify-email/{token}/'
            )
            send_mail(
                'Verify your email',
                f'Click the link to verify your email: {verification_link}',
                'swskye17@gmail.com',  # From email
                [user.email],  # To email
                fail_silently=False,
            )
            messages.success(
                request, 'Registration successful! Please check your email to verify your account.')

            # login(request, user)
            # Send a welcome email
            send_mail(
                'Welcome to Agrimax',
                'Thank you for registering!',
                'swskye17@gmail.com',  # From email
                [user.email],  # To email
                fail_silently=False,
            )'''
            login(request, user)
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('home')  # Redirect to the login page

        else:
            messages.error(request, form.errors)

    else:
        # print(form.errors)
        form = CustomRegistrationForm()
        messages.error(request, 'Bad request')
    return render(request, 'signup.html', {'form': form})


# accounts/views.py
def verify_email(request, token):
    try:
        profile = Profile.objects.get(verification_token=token)
        user = profile.user
        user.is_active = True  # Activate the user account
        user.save()
        profile.verification_token = None  # Clear the token after verification
        profile.save()
        messages.success(
            request, 'Email verified successfully! You can now log in.')
        return redirect('login')  # Redirect to login page
    except Profile.DoesNotExist:
        messages.error(request, 'Invalid verification link.')
        return redirect('login')


@login_required
def user_logout(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return HttpResponseRedirect(reverse('userlogin'))


def recommend(request):
    from .CRecommend import controller
    if request.method == 'POST':
        form = FarmDataForm(request.POST)
        # print(request.POST)
        if form.is_valid():
            _N = form.cleaned_data['_N']
            model = form.cleaned_data['model']
            potassium = form.cleaned_data['potassium']
            phosphorus = form.cleaned_data['phosphorus']
            nitrogen = form.cleaned_data['nitrogen']
            ph = form.cleaned_data['ph']
            temperature = form.cleaned_data['temperature']
            rainfall = form.cleaned_data['rainfall']
            humidity = form.cleaned_data['humidity']

            if model == "all":
                model = None

            crop_rec = controller(
                nitrogen, phosphorus, potassium, temperature, humidity, ph, rainfall, _N, model)

            # Store in session
            request.session['crop_rec'] = crop_rec
            return redirect(f"{reverse('home_crop_rec')}#crop_rec")
        else:
            return render(request, 'index.html', {'form': form})
            # return HttpResponse('<b>Invalid form</b>')
    else:
        form = FarmDataForm()
        return redirect("/home/#crop-recommendation")


def healthEval(request):
    if request.method == 'POST':
        form = HealthDataForm(request.POST)
        if form.is_valid():
            crop = form.cleaned_data['desired_crop']
            potassium = form.cleaned_data['potassium']
            phosphorus = form.cleaned_data['phosphorus']
            nitrogen = form.cleaned_data['nitrogen']
            ph = form.cleaned_data['ph']

            if crop == 'all':
                crop = None

            health = Health()
            recommendations = health.evaluate_soil_health(
                float(nitrogen), float(phosphorus), float(potassium), float(ph), crop)

            # Store in session
            request.session['recommendations'] = recommendations
            return redirect(f"{reverse('home_rec')}#soil-health")
        else:
            return messages.error(request, '<b>Invalid form</b>')
    else:
        form = HealthDataForm()
        return redirect(f"{reverse('home')}#soil-health")
    pass
