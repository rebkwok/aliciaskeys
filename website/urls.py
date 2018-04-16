from django.urls import path

from website.views import clinics, contact, home, privacy_policy, underconstruction


app_name = 'website'


urlpatterns = [
    path('contact/', contact, name='contact'),
    path('elite-performance-clinics/', clinics, name='clinics'),
    path('privacy-policy/', privacy_policy, name='privacy_policy'),
    path('aajskfhansfmalkj', home, name='home'),
    path('', underconstruction, name='underconstruction')
]
