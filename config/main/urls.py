from django.urls import path

from .views import contact_view, home_view, service_detail_view

urlpatterns = [
    path('', home_view, name='home'),
    path('contact/', contact_view, name='contact'),
    path('service/<slug:slug>/', service_detail_view, name='service_detail'),
]
