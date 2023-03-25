from django.urls import path
from .views import *
app_name = "home"
urlpatterns = [
    path('', login_vue),
    path('principal', principal_vue, name="principal"),
    path('creation', creation_vue, name="creation")
]