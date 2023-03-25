# from django.db import models

# Create your models here.
class personne:
    def __init__(self, prenom, nom, sexe):
        self.prenom = prenom
        self.nom = nom
        self.sexe = sexe
    class Meta:
        abstract = True

class client(personne):
    def __init__(self, prenom, nom, sexe, incription, courriel, motdepasse):
        super().__init__(prenom,nom,sexe)
        self.incription = incription
        self.courriel = courriel
        self.motdepasse = motdepasse
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
        self.motdepasse = motdepasse
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