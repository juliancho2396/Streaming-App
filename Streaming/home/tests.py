from django.test import SimpleTestCase
from .models import *
from .views import *

# Créer les testes ici
class ApplicationTestCase(SimpleTestCase):


    def test_initial(self):
        temporaire = {
            'usagers': []
        }


        # Si le retour est faux, c'est à cause de que le courriel est déjà enregistré


        # Ajoute des clients pour la premiere fois

        temporaire = enregistrer_usager(temporaire, client('Julian', 'Munoz', 'M', 'Aujourd hui', 'julianemail@limoilu.com', 'motdEpasse1'))
        self.assertTrue(temporaire)
        temporaire = enregistrer_usager(temporaire, client('Sebastien', 'Bustamante', 'M', 'Aujourd hui', 'julianemail3@limoilu.com', 'mOtdep4sse'))
        self.assertTrue(temporaire)

            # Teste si ne permet pas enregistrer des courriels existants
        with self.assertRaises(ValueError):
            enregistrer_usager(temporaire, client('Johanna', 'Harris', 'F', 'Hier', 'julianemail@limoilu.com', 'mOtdep4sse3'))

            # Teste si ne permet pas enregistrer des mots de passe non sécuritaires
        with self.assertRaises(ValueError):
            enregistrer_usager(temporaire, client('Johanna', 'Harris', 'F', 'Hier', 'jharris@limoilu.com', 'mot123'))


        # Confirme le fonctionnement de l'authentification
        self.assertTrue(authentifier_usager(temporaire, 'julianemail@limoilu.com', 'motdEpasse1'))
        self.assertTrue(authentifier_usager(temporaire, 'julianemail3@limoilu.com', 'mOtdep4sse'))

        with self.assertRaises(ValueError):
            self.assertFalse(authentifier_usager(temporaire, 'julianemail@limoilu.com', 'motdEpasse'))
            self.assertFalse(authentifier_usager(temporaire, 'julianemail@limoiu.com', 'motdE'))


