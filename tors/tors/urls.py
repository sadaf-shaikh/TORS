"""tors URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from tors_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name="index"),
    path('view/<int:tour_id>/', views.tour_info,name="view_tour"),
    path('reserve/<int:tour_id>/', views.reserve_tour,name="reserve_tour"),
    path('login/', views.tors_login, name="tors_login"),
    path('home/', views.cutomer_home, name="home"),
    path('view_reservation/<int:reserve_id>/', views.reservation_info, name="r_info"),
    path('cancel_reservation/<int:reserve_id>/', views.cancel_tour, name="cancel_tour"),
    path('feedback/', views.feedback, name="feedback"),





    
]
