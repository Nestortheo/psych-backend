from django.urls import path
from .views import contact_submit

urlpatterns = [
    path('send/', contact_submit, name='contact'),
]
