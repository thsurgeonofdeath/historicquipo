from django.urls import path
from routing.views import home

app_name = 'routing'

urlpatterns = [
    path('calculator/', home, name='homepage'),
]