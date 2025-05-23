
"""Vendorsinprojectversion2 URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken import views  # import rest_framework authtoken

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-token-auth/', views.obtain_auth_token),  # rest_framework authtoken url
    path('self-register/',include('RegistrationApp.urls')), # registrationapp urls
    path('masters/',include('MastersApp.urls')),
    path('materials/',include('MaterialApp.urls')),
    path('landing-page/',include('LandingPageApp.urls')),
    path('dashboard-page/',include('DashboardApp.urls')),
    path('bidding/',include('BiddingApp.urls')),
    path('admin-page/',include('AdminApp.urls')),
    path('subscriptions/',include('SubscriptionApp.urls'))
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)