from django.urls import path
from .views import (
    home_page, car_list, car_detail, admin_dashboard,
    new_cars, used_cars, services, pricing, about, contact
)

urlpatterns = [
    path("", home_page, name='home'),
    path("avtomobillar/", car_list, name='car_list'),
    path("avtomobil/<int:car_id>/", car_detail, name='car_detail'),
    path("yangi/", new_cars, name='new_cars'),
    path("ishlatilgan/", used_cars, name='used_cars'),
    path("xizmatlar/", services, name='services'),
    path("narxlar/", pricing, name='pricing'),
    path("biz-haqimizda/", about, name='about'),
    path("aloqa/", contact, name='contact'),
    path("admin-dashboard/", admin_dashboard, name='admin_dashboard'),
]
