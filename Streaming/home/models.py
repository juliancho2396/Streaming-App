# from django.db import models
from django.contrib.auth.hashers import make_password

# Create your models here.
class personne:
    def __init__(self, prenom, nom, sexe):
        self.prenom = prenom
        self.nom = nom
        self.sexe = sexe
    class Meta:
        abstract = True

# confirme si il y a des numéros, majuscules et minuscules
def motdepasse_securitaire(motdepasse):
    if len(motdepasse) < 8:
        return False
    if not any(char.isdigit() for char in motdepasse):
        return False
    if not any(char.isalpha() for char in motdepasse):
        return False
    if not any(char.isupper() for char in motdepasse):
        return False
    return True

class client(personne):
    def __init__(self, prenom, nom, sexe, incription, courriel, motdepasse):
        super().__init__(prenom,nom,sexe)
        self.incription = incription
        self.courriel = courriel
        if motdepasse_securitaire(motdepasse):
            self.motdepasse = make_password(motdepasse)
        else:
            raise ValueError("Le mot de passe n'est pas assez sécuritaire")
        self.cartes_de_credit = []

    def ajouter_carte_de_credit(self, numero, expiration):
        for carte in self.cartes_de_credit:
            if carte.numero == numero:
                return False
        carte = cartedecredit(numero=numero, expiration=expiration)
        self.cartes_de_credit.append(carte)
        return True
        

class employe(personne):
    def __init__(self, prenom, nom, sexe, embauche, utilisateur, motdepasse, typeacces):
        super().__init__(prenom,nom,sexe)
        self.embauche = embauche
        self.utilisateur = utilisateur
        if motdepasse_securitaire(motdepasse):
            self.motdepasse = make_password(motdepasse)
        else:
            raise ValueError("Le mot de passe n'est pas assez sécuritaire")
        self.typeacces = typeacces

class acteur(personne):
    def __init__(self, prenom, nom, sexe, nompersonnage, debutemploi, finemploi, cachet):
        super().__init__(prenom,nom,sexe)
        self.nompersonnage = nompersonnage
        self.debutemploi = debutemploi
        self.finemploi = finemploi
        self.cachet = cachet
        self.films = []

class cartedecredit:
    def __init__(self, numero, expiration):
        self.numero = numero
        self.expiration = expiration


class categorie:
    def __init__(self, nom, description):
        self.nom = nom
        self.description = description

class film:
    def __init__(self, nom, duree, description):
        self.nom = nom
        self.duree = duree
        self.description = description
        self.categories = []
        self.acteurs = []

    def ajouter_categorie(self, nom, description):
        for cat in self.categories:
            if cat.nom == nom:
                return False
        cat = categorie(nom=nom, description=description)
        self.categories.append(cat)
        return True

    def ajouter_acteur(self, prenom, nom, sexe, nompersonnage, debutemploi, finemploi, cachet):
        for act in self.acteurs:
            if act.prenom == prenom and act.nom == nom and act.sexe == sexe and act.nompersonnage == nompersonnage:
                return False
        act = acteur(prenom=prenom, nom=nom, sexe=sexe, nompersonnage=nompersonnage, debutemploi=debutemploi, finemploi=finemploi, cachet=cachet)
        self.categories.append(act)
        return True