from django.shortcuts import render, redirect, reverse
from django.contrib.auth.hashers import check_password
from .models import *


def login_vue(request):
    # nous initialisons un contexte temporaire. Il faut enlever une fois qu'on utilise une base de donnes
    context = charger_context()
    if request.method == "POST":
        try:
            context['session'] = authentifier_employe(context, request.POST['username'], request.POST['password'])
            # Une fois qu'une base de donnes es utiliser. SVP utiliser une redirection plus adaptee au besoin.
            return principal_vue(request, context=context)
        except ValueError as error:
            # Ajoute les erreur a montrer a l'usager
            context['errors'].append(error)
    return render(request, 'login.html', context)

def principal_vue(request, context):
    # facon de montrer la fenetre principale
    return render(request, 'principal.html', context=context)

def creation_vue(request):
    # Charge contexte temporaire
    context = charger_context()
    if request.method == "POST":
        try:
            # Faite la validation des mots de passe et sa confirmation (doivent etre identiques)
            validation_mdp = request.POST['password'] == request.POST['confirm-password']
            if not validation_mdp:
                context['errors'].append('La confirmation de mot de passe doit être identique que votre mot de passe.')

            # Si la validation des mot de passe est reusie, aussi que l'enregistrement du nouveau employe, la fenetre principale est montree.
            if validation_mdp and enregistrer_employe(context, employe(request.POST['firstname'], request.POST['lastname'], request.POST['sex'], datetime.date.today().strftime('%m-%y') , request.POST['email'], request.POST['password'], request.POST['typeacces'])):
                # a remplacer quand l'application se connecte avec une base de donnees.
                return render(request, 'principal.html', context)

        # S'il y a quelque erreur dans la procedure, il l'ajoute pour le montrer a l'usager.
        except ValueError as error:
            context['errors'].append(error)
    # Imprime la page de creation de nouveaux mais en montrant les erreurs.
    return render(request, 'creation.html', context)


def creation_client(request):
    # Charge contexte temporaire
    context = charger_context()
    if not request.method == "POST":
        return redirect('home:home')

    try:
        # Faite la validation des mots de passe et sa confirmation (doivent etre identiques)
        validation_mdp = request.POST['Password'] == request.POST['PasswordConfirmation']

        if not validation_mdp:
            context['errors'].append('La confirmation de mot de passe doit être identique que votre mot de passe.')

        else:

            context = enregistrer_client(context, client(request.POST['prenomclient'], request.POST['prenomclient'],
                                                         request.POST['sex'],
                                                         request.POST['email'], request.POST['Password'],
                                                         ))
        # Si la validation des mot de passe est reusie, aussi que l'enregistrement du nouveau employe, la fenetre principale est montree.
        return render(request, 'principal.html', context)

    except ValueError as error:
        # ajoute les erreurs a montre sur le frontend.
        context['errors'].append(error)

def modifier_client(request, courriel):
    # Charge contexte temporaire
    context = charger_context()

    # Identifie si le formulaire va se montrer pour la premier fois ou si est en train de recevoir les modifications.
    # S'il recois des modifications, il est True, sinon False
    modifier = all(field in request.POST for field in ['prenomclient', 'nomclient', 'sexe', 'email'])

    # Fonction pour chercher le clients dans la variable contenant les clients enregistres au systeme (contexte temporaire).
    info_client = None
    for client in context['clients']:
        if client.courriel == courriel:
            info_client = client
    if modifier == True:
        # Fais la validation si le courriel a ete modifier. si oui, verifie si le nouveau n'est pas deja utilise.
        # En cas que le courriel existe deja, returne un erreur.
        if not request.POST['email'] == info_client.courriel and request.POST['email'] in [client.courriel for client in context['clients']]:
            context['errors'].append('Le courriel est deja enregistré dans le système.')
        try:
            # Execute la modification des informations.
            info_client.mettre_a_jour(request.POST['prenomclient'], request.POST['nomclient'], request.POST['sexe'], request.POST['email'])

        except ValueError as error:
            # en cas d'erreur, il est ajouter au contexte pour etre montre.
            context['errors'].append(error)
    context['client'] = info_client
    return render(request, 'modifierclient.html', context)


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
    enregistrer_client(context, client('Fernando', 'Martone', 'M', 'fmartone@limoilu.com', 'Motdepasse3'))
    Film = film("Le Parrain", 197, "Produit par les studios Paramount, le film est l'adaptation du roman du même nom (1969) écrit par le romancier Mario Puzo. L'histoire se déroule à New York sur une période allant de 1945 à 1955, et raconte les luttes de pouvoir au sein de la mafia américaine new-yorkaise, avec pour protagoniste principal la famille Corleone, l'une des cinq familles mafieuses de la ville, la famille Corleone étant menée par son patriarche, Don Vito Corleone dit le « Parrain » (Marlon Brando), un personnage puissant et influent")
    enregistrer_film(context, Film)
    Film.ajouter_acteur(acteur("Marlon", "Brando", "M", "Don Vito Corleone", "12-85", "", "Paramount"))
    Film.ajouter_acteur(acteur("Al", "Pacino", "M", "Michael Corleone", "08-80", "", "Paramount"))
    Film.ajouter_categorie("Viex", "Films tres vieux")
    Film.ajouter_categorie("Mafias", "Films avec contenus de mafias")
    return context



# Manipulation des classes. Dans ce cas, le methode recoit juste la classe
def enregistrer_employe(temporaire, nouveau):
    # een utilisant le contexte temporaire, un employe est ajoute.
    for usager in temporaire['usagers']:
        # Si le courriel est déjà utilisé, il retourne faux et l'ajoute pas
        if usager.utilisateur == nouveau.utilisateur:
            raise ValueError("Courriel déjà utilisé")
    temporaire['usagers'].append(nouveau)
    return temporaire



def enregistrer_client(temporaire, nouveau):
    # een utilisant le contexte temporaire, un client est ajoute.
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