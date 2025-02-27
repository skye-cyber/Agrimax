"""
URL configuration for AgriMax project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from AgriMaxApp import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path("admin", admin.site.urls),
    path("getlogin", views.get_loginPage, name="getlogin"),
    path("", views.user_login, name="userlogin"),
    path("gethome/", views.get_homePage, name="home"),
    path(
        "home_h_rec/", views.get_homePage_rec, name="home_rec"
    ),  # home with recommendation
    path("getsignup/", views.get_signupPage, name="getsignup"),
    path("home_crop_rec/", views.get_homePage_crop_rec, name="home_crop_rec"),
    path("usersignup/", views.signup, name="usersignup"),
    path("logout/", views.user_logout, name="logout"),
    path("verify-email/<uuid:token>/", views.verify_email, name="verify_email"),
    path("gethistory/", views.get_historyPage, name="history"),
    path("getweather/", views.get_weather_page, name="weather"),
    path("recommend/", views.recommend, name="recommend"),
    path("health/", views.healthEval, name="health"),
    path("farm&information/", views.FarminfoHandler, name="farminformation"),
    path("getFarmPage/", views.getFarmPage, name="farmPage"),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
