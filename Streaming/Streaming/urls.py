from django.contrib import admin
from django.urls import path, include

# ici il faut relier les routes et/ou endpoints de notre application web
urlpatterns = [
    # admin a besoin d'une base de données.
    # dans le cas de relier fichier urls d'un autre module, svp enregistrez le dans settings.py[´INSTALLED_APPS´]
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
]
