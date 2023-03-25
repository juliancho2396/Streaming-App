from django.test import SimpleTestCase
from .models import *
from .views import *

# Créer les testes ici
class ApplicationTestCase(SimpleTestCase):


    def test_initial(self):
        usagers = []
        def ajouter(nouveau):
            for usager in usagers:
                if usager.courriel == nouveau.courriel:
                    return False
            usagers.append(nouveau)
            return True

        # Si le retour est faux, c'est à cause de que le courriel est déjà enregistré
        self.assertTrue(ajouter(client('Julian', 'Munoz', 'M', 'Aujourd hui', 'julianemail', 'mdp')))
        self.assertTrue(ajouter(client('Sebastien', 'Bustamante', 'M', 'Aujourd hui', 'julianemail3', 'mdp')))
        self.assertTrue(ajouter(client('Julian', 'Munoz', 'M', 'Aujourd hui', 'julianemail4', 'mdp')))

