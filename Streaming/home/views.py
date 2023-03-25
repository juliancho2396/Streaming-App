from django.shortcuts import render, redirect, reverse
from django.contrib.auth.hashers import check_password
from .models import *
# Create your views here.
def login_vue(request):
    context = charger_context()
    if request.method == "POST":

        return redirect('home:principal')
    return render(request, 'login.html')

def principal_vue(request):
    context = charger_context()
    return render(request, 'principal.html')

def creation_vue(request):
    context = charger_context()
    if request.method == "POST":
        return redirect('home:principal')
    return render(request, 'creation.html')

def modification_vue(request):
    context = charger_context()
    if request.method == "POST":
        return redirect('home:principal')
    return render(request, 'creation.html')


# Cars il n'y as pas une base de données, nous allons utiliser cette fonction pour sauvegarder information temporairement
def charger_context():
    context = {
        'usagers': []
    }
    enregistrer_usager(context, client('Sebastien', 'Bustamante', 'M', 'Aujourd hui', 'julianemail3@limoilu.com', 'mOtdep4sse'))
    return context



# Manipulation des classes
def enregistrer_usager(temporaire, nouveau):

    for usager in temporaire['usagers']:
        # Si le courriel est déjà utilisé, il retourne faux et l'ajoute pas
        if usager.courriel == nouveau.courriel:
            raise ValueError("Courriel déjà utilisé")
    temporaire['usagers'].append(nouveau)
    return temporaire

def authentifier_usager(temporaire, courriel, mdp):
    for usager in temporaire['usagers']:
        if usager.courriel == courriel:
            if check_password(mdp, usager.motdepasse):
                return True
    raise ValueError("Utilisateur ou mot de passe incorrect")
