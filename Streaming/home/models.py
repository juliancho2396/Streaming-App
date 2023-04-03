# from django.db import models
from django.contrib.auth.hashers import make_password
import datetime

# Create your models here.
class personne:
    def __init__(self, prenom, nom, sexe):
        self.prenom = prenom
        self.nom = nom
        if not sexe in ['M', 'F', 'A']:
            raise ValueError("Le genre d'une personne doit être M, F ou A")
        self.sexe = sexe
    class Meta:
        abstract = True
    def __str__(self) -> str:
        return " ".join([self.prenom, self.nom])

# confirme si il y a des numéros, majuscules et minuscules
def motdepasse_securitaire(motdepasse):
    if len(motdepasse) < 8:
        raise ValueError("Le mot de passe n'est pas assez sécuritaire")
    if not any(char.isdigit() for char in motdepasse):
        raise ValueError("Le mot de passe n'est pas assez sécuritaire")
    if not any(char.isalpha() for char in motdepasse):
        raise ValueError("Le mot de passe n'est pas assez sécuritaire")
    if not any(char.isupper() for char in motdepasse):
        raise ValueError("Le mot de passe n'est pas assez sécuritaire")
    return True


def date_valide(entree):
    if any(char.isalpha() for char in (element for element in entree.split('-'))) or not len(entree.split('-')) == 2 or int(entree.split('-')[1]) > 99 or int(entree.split('-')[0]) > 12:
        raise ValueError("Date ou format incorrect. Il faut utiliser le format MM-YY")

def non_expiree(entree):
    if datetime.date(day=1, month=int(entree.split('-')[0]), year=int(entree.split('-')[1]) + 2000) < datetime.date.today():
            raise ValueError("Carte expiree. Il faut utiliser le format MM-YY")

def champs_remplis(liste):
    if any(str(texte).strip() == '' for texte in liste): # Il faut laisser str(texte) sinon le code ne va pas marcher si nous introduisons chiffres
        raise ValueError("Tous les champs doivent être remplis")

class client(personne):
    def __init__(self, prenom, nom, sexe, courriel, motdepasse):
        # confirme si tous les champs sont remplis
        champs_remplis([prenom, nom, sexe, courriel, motdepasse])
        super().__init__(prenom,nom,sexe)
        if not '@' in courriel or not '.' in courriel or ' ' in courriel:
            raise ValueError("Introduissez une adresse courriel valide.")
        self.incription = datetime.date.today()
        self.courriel = courriel
        motdepasse_securitaire(motdepasse)
        self.motdepasse = make_password(motdepasse)
        self.cartes_de_credit = []

    def ajouter_carte_de_credit(self, numero, expiration):
        date_valide(expiration)
        non_expiree(expiration)
        for carte in self.cartes_de_credit:
            # Si la carte est déjà ajourté pour cet utilisateur, la date d'expiration s'est mis à jour
            if carte.numero == numero:
                carte.mettre_a_jour_expiration(expiration)
                return True
        carte = cartedecredit(numero=numero, expiration=expiration)
        self.cartes_de_credit.append(carte)
        return True
        

class employe(personne):
    def __init__(self, prenom, nom, sexe, embauche, utilisateur, motdepasse, typeacces):
        champs_remplis([prenom, nom, sexe, utilisateur, motdepasse, typeacces])
        date_valide(embauche)
        super().__init__(prenom,nom,sexe)
        self.embauche = embauche
        if not '@' in utilisateur or not '.' in utilisateur or ' ' in utilisateur:
            raise ValueError("Introduissez une adresse courriel valide.")
        self.utilisateur = utilisateur
        if motdepasse_securitaire(motdepasse):
            self.motdepasse = make_password(motdepasse)
        else:
            raise ValueError("Le mot de passe n'est pas assez sécuritaire")
        if typeacces in ['0', '1']:
            self.typeacces = typeacces
        else:
            raise ValueError("Type d'acces n'est pas valide.")

class acteur(personne):
    def __init__(self, prenom, nom, sexe, nompersonnage, debutemploi, finemploi, cachet):
        champs_remplis([prenom, nom, sexe, nompersonnage, debutemploi, cachet])
        date_valide(debutemploi)
        if not finemploi == "" and not finemploi == None:
            date_valide(finemploi)
        super().__init__(prenom,nom,sexe)
        self.nompersonnage = nompersonnage
        self.debutemploi = debutemploi
        self.finemploi = finemploi
        self.cachet = cachet
    def __str__(self) -> str:
        return super().__str__()


class cartedecredit:
    def __init__(self, numero, expiration):
        if any(char.isalpha() for char in numero) or not len(numero) == 16:
            raise ValueError("Numéro de carte doit comprendre 16 chiffres et ne peut pas avoir des symboles.")
        date_valide(expiration)
        non_expiree(expiration)
        
        self.numero = numero
        self.expiration = expiration

    def mettre_a_jour_expiration(self, expiration):
        date_valide(expiration)
        self.expiration = expiration


class categorie:
    def __init__(self, nom, description):
        self.nom = nom
        self.description = description
    def __str__(self) -> str:
        return self.nom

class film:
    def __init__(self, nom, duree, description):
        champs_remplis([nom, description])
        if not type(duree) == int:
            raise ValueError("Dureé doit être numérique.")
        self.nom = nom
        self.duree = duree
        self.description = description
        self.categories = []
        self.acteurs = []

    def ajouter_categorie(self, nom, description):
        champs_remplis([nom, description])
        for cat in self.categories:
            if cat.nom == nom:
                return False
        cat = categorie(nom=nom, description=description)
        self.categories.append(cat)
        return True

    def ajouter_acteur(self, artiste):
        
        for act in self.acteurs:
            if act.prenom == artiste.prenom and act.nom == artiste.nom and act.sexe == artiste.sexe and act.nompersonnage == artiste.nompersonnage:
                return True
        self.acteurs.append(artiste)
        return True