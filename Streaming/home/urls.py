from django.urls import path
from .views import *
app_name = "home"
urlpatterns = [
    path('', login_vue, name="home"),
    path('principal', principal_vue, name="principal"),
    path('creation', creation_vue, name="creation"),
    path('creationclient', creation_client, name="creation_client"),
    path('modifierclient/<str:courriel>', modifier_client, name="modifier_client")

]