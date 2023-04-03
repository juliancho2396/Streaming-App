from django.shortcuts import render, redirect, reverse
from django.contrib.auth.hashers import check_password
from .models import *
# Create your views here.
def login_vue(request):
    context = charger_context()
    if request.method == "POST":
        try:
            context['session'] = authentifier_employe(context, request.POST['username'], request.POST['password'])
            return principal_vue(request, context)
        except ValueError as error:
            context['errors'].append(error)
    return render(request, 'login.html', context)

def principal_vue(request, context):
    
    
    return render(request, 'principal.html', context)

def creation_vue(request):
    context = charger_context()
    if request.method == "POST":
        if request.method == "POST":
            try:
                validation_mdp = request.POST['password'] == request.POST['confirm-password']
                if not validation_mdp:
                    context['errors'].append('La confirmation de mot de passe doit être identique que votre mot de passe.')
                if validation_mdp and enregistrer_client(context, client(request.POST['firstname'], request.POST['lastname'], request.POST['sex'], request.POST['email'], request.POST['password'])):
                    return redirect('home:home')
            except ValueError as error:
                context['errors'].append(error)

    return render(request, 'creation.html', context)

def modification_vue(request):
    context = charger_context()
    if request.method == "POST":
        return redirect('home:principal')
    return render(request, 'creation.html')


# Cars il n'y as pas une base de données, nous allons utiliser cette fonction pour sauvegarder information temporairement
def charger_context():
    context = {
        'usagers': [],
        'errors' : [],
        'clients' : [],
        'session': [],
        'films': [],
    }
    enregistrer_employe(context, employe('Julian', 'Munoz', 'M', '01-01', 'julianemail@limoilu.com', 'motdEpasse1', '1'))
    enregistrer_employe(context, employe('Sebastien', 'Bustamante', 'M', '01-03', 'julianemail3@limoilu.com', 'mOtdep4sse', '0'))
    enregistrer_client(context, client('Alice', 'Dupont', 'F', 'alice@limoilu.com', 'Motdepasse1'))
    Film = film("Le Parrain", 197, "Produit par les studios Paramount, le film est l'adaptation du roman du même nom (1969) écrit par le romancier Mario Puzo. L'histoire se déroule à New York sur une période allant de 1945 à 1955, et raconte les luttes de pouvoir au sein de la mafia américaine new-yorkaise, avec pour protagoniste principal la famille Corleone, l'une des cinq familles mafieuses de la ville, la famille Corleone étant menée par son patriarche, Don Vito Corleone dit le « Parrain » (Marlon Brando), un personnage puissant et influent")
    enregistrer_film(context, Film)
    Film.ajouter_acteur(acteur("Marlon", "Brando", "M", "Don Vito Corleone", "12-85", "", "Paramount"))
    Film.ajouter_acteur(acteur("Al", "Pacino", "M", "Michael Corleone", "08-80", "", "Paramount"))
    Film.ajouter_categorie("Viex", "Films tres vieux")
    Film.ajouter_categorie("Mafias", "Films avec contenus de mafias")
    return context



# Manipulation des classes. Dans ce cas, le methode recoit juste la classe
def enregistrer_employe(temporaire, nouveau):

    for usager in temporaire['usagers']:
        # Si le courriel est déjà utilisé, il retourne faux et l'ajoute pas
        if usager.utilisateur == nouveau.utilisateur:
            raise ValueError("Courriel déjà utilisé")
    temporaire['usagers'].append(nouveau)
    return temporaire



def enregistrer_client(temporaire, nouveau):

    for usager in temporaire['clients']:
        # Si le courriel est déjà utilisé, il retourne faux et l'ajoute pas
        if usager.courriel == nouveau.courriel:
            raise ValueError("Courriel déjà utilisé")
    temporaire['clients'].append(nouveau)
    return temporaire

def authentifier_employe(temporaire, utilisateur, mdp):
    for usager in temporaire['usagers']:
        if usager.utilisateur == utilisateur:
            if check_password(mdp, usager.motdepasse):
                return usager
    raise ValueError("Utilisateur ou mot de passe incorrect")

def enregistrer_carte(temporaire, courriel, numerocarte, expiration):
    if courriel == '' or numerocarte == '' or expiration =='':
        raise ValueError("Pour enregistrer une carte de crédit, il faut remplir tous les champs.")
    for usager in temporaire['clients']:
        if usager.courriel == courriel:
            usager.ajouter_carte_de_credit(numerocarte, expiration)
            return True
    raise ValueError("Le courriel indiqué n'est pas enregistré.")

def enregistrer_film(temporaire, nouveau):

    for film in temporaire['films']:
        # Si le courriel est déjà utilisé, il retourne faux et l'ajoute pas
        if film.nom == nouveau.nom:
            raise ValueError("Film déjà enregistré.")
    temporaire['films'].append(nouveau)
    return temporaire