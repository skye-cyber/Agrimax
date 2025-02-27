import asyncio
from datetime import datetime
from django.db.models import QuerySet
# from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout  # get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm  # , UserCreationForm
# from django.contrib.auth.models import User
# from django.core.mail import send_mail
from django.http import (HttpResponse, HttpResponseBadRequest,
                         HttpResponseForbidden, HttpResponseRedirect,
                         JsonResponse, StreamingHttpResponse)
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django_ratelimit.decorators import ratelimit

from .analytics import Draw
from .forms import (CustomRegistrationForm, FarmDataForm, FarmInformationForm,
                    HealthDataForm)
from .health import Health
from .models import CustomUser, FarmInformation, Profile
from .Weather import main

# from .forms import CustomRegistrationForm

# Create your views here.


def get_loginPage(request):
    return render(request, "login.html")


def get_signupPage(request):
    return render(request, "signup.html")


def getFarmPage(request):
    return redirect("farminformation")


def GetFarmDetail(request, names=False, locations=False):
    """
    Fetch farm details for the currently logged-in user.
    If no flags (names or locations) are provided, return all data in dictionary form.
    """
    if not request.user.is_authenticated:
        return None  # Return None if the user is not authenticated

    farms = FarmInformation.objects.filter(user=request.user)  # Filter farms for the current user

    if not farms:
        return None  # Return None if no farms are found

    if not names and not locations:
        # Return all data in dictionary form
        all_data = [farm.__dict__ for farm in farms]
        for farm_data in all_data:
            farm_data.pop('_state', None)  # Remove the _state attribute if it exists
        return all_data

    if locations:
        if isinstance(farms, QuerySet):
            locations = list(farms.values_list('farm_location', flat=True))
        else:
            locations = [data.farm_location for data in farms]
    else:
        if isinstance(farms, QuerySet):
            locations = list(farms.values_list('farm_name', flat=True))
        else:
            locations = [data.farm_name for data in farms]

    # print(locations)
    return locations


def get_weather_page(request):
    # Get all locations from the database or source
    # Ensure this function returns a list of locations
    locations = GetFarmDetail(request, locations=True)
    farmNames = GetFarmDetail(request, names=True)
    weather_data_list = []
    error_locations = []

    # Fetch weather data for each location
    if locations:
        for loc, farmName in zip(locations, farmNames):
            try:
                # Retrieve weather data for the current location
                weekly_data = main(loc)
                hourly_data = main(loc, _type='hourly3')

                # Check for API errors
                if isinstance(weekly_data, str) and weekly_data in ("RequestFailure", "ConnectionError"):
                    error_locations.append({"location": loc, "error": weekly_data})
                    continue
                if isinstance(hourly_data, str) and hourly_data in ("RequestFailure", "ConnectionError"):
                    error_locations.append({"location": loc, "error": hourly_data})
                    continue

                # Process and format weather data
                weather_data = {
                    "farmName": farmName,
                    "location": hourly_data.get("name"),
                    "country": hourly_data["sys"].get("country"),
                    # Convert to Celsius
                    "temperature": hourly_data["main"].get("temp") - 273.15,
                    "icon": hourly_data["weather"][0].get("icon"),
                    "visibility": hourly_data["visibility"],
                    "feels_like": hourly_data["main"].get("feels_like") - 273.15,
                    "humidity": hourly_data["main"].get("humidity"),
                    "pressure": hourly_data["main"].get("pressure"),
                    "wind_speed": hourly_data["wind"].get("speed"),
                    "wind_direction": hourly_data["wind"].get("deg"),
                    "weather_main": hourly_data["weather"][0].get("main"),
                    "weather_description": hourly_data["weather"][0].get("description"),
                    "rain_last_hour": hourly_data.get("rain", {}).get("1h", 0),
                    "cloud_cover": hourly_data["clouds"].get("all"),
                    "sunrise": datetime.fromtimestamp(hourly_data["sys"].get("sunrise")).strftime("%H:%M:%S"),
                    "sunset": datetime.fromtimestamp(hourly_data["sys"].get("sunset")).strftime("%H:%M:%S"),
                    "weekly": weekly_data,  # Weekly forecast data
                }

                # Append processed data to the list
                weather_data_list.append(weather_data)

            except Exception as e:
                # Log errors for debugging
                raise
                error_locations.append({"location": loc, "error": str(e)})

        # Render the data in the template
        context = {
            "weather_data_list": weather_data_list
        }
        if error_locations and weather_data_list == []:
            return render(request, 'error.html', {"error_message": error_locations}, status=404)
        return render(request, 'weather.html', context)
    else:
        return render(request, 'error.html', {'error_message': 'Could not obtain Forecast: -> No Farm Locations set!'}, status=404)


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
    analytics = request.session.get('analytics', {})
    # Clear the recommendations from the session if you don't need it anymore
    if 'crop_rec' in request.session:
        del request.session['crop_rec']
    if 'analytics' in request.session:
        del request.session['analytics']

    elif analytics is None:
        analytics = 'error: No analytics data available.'

    return render(request, "index.html", {'crop_rec': crop_rec, 'analytics': analytics})


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
        form = CustomRegistrationForm(request.POST)  # Bind form with POST data
        if form.is_valid():
            user = form.save()
            login(request, user)
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('farminformation')  # Redirect to the Farm Information form
        else:
            # Pass errors back to the template
            messages.error(request, 'There were errors in your form.')
    else:
        form = CustomRegistrationForm()
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


# Farm Information View
def FarminfoHandler(request):
    if request.method == 'POST':
        form = FarmInformationForm(request.POST)
        if form.is_valid():
            farm_info = form.save(commit=False)
            farm_info.user = request.user  # Automatically set the user field
            farm_info.save()
            return redirect('home')
        else:
            messages.error(request, 'There were errors in your form.')
    else:
        form = FarmInformationForm()

    return render(request, 'farm-details.html', {'form': form})


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
            init = Draw(crop_rec)
            analytics = asyncio.run(init.fetchAll())

            request.session['analytics'] = analytics
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

            print(recommendations)
            """init = Draw(recommendations)
            analytics = asyncio.run(init.fetchAll())

            request.session['analytics'] = analytics"""

            return redirect(f"{reverse('home_rec')}#soil-health")
        else:
            return messages.error(request, '<b>Invalid form</b>')
    else:
        form = HealthDataForm()
        return redirect(f"{reverse('home')}#soil-health")
    pass
