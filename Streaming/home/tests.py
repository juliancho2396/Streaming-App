from django.test import SimpleTestCase
from .models import *
from .views import *


class ApplicationTestCase(SimpleTestCase):

    def setUp(self):
        # Crea un objeto de temporario antes de cada test
        self.temporaire = {
            'usagers': [],
            'clients': [],
            'films': [],
        }

    def test_enregistrer_employe(self):
        # Asegura que se pueda agregar empleados
        self.assertTrue(enregistrer_employe(self.temporaire, employe('Julian', 'Munoz', 'M', '01-01', 'julianemail@limoilu.com', 'motdEpasse1', '1')))
        self.assertTrue(enregistrer_employe(self.temporaire, employe('Sebastien', 'Bustamante', 'M', '01-03', 'julianemail3@limoilu.com', 'mOtdep4sse', '0')))

        # Asegura que no se pueda agregar empleados con campos vacíos
        with self.assertRaises(ValueError):
            enregistrer_employe(self.temporaire, employe('Johanna', 'Harris', 'F', '01-12', 'julianemail@limoilu.com', 'mOtdep4sse3', ''))
        with self.assertRaises(ValueError):
            enregistrer_employe(self.temporaire, employe('Louis', 'A', 'F', '01-16', 'lou iseh@limoilu.com', 'mOtdep4sse3', '1'))
        with self.assertRaises(ValueError):
            enregistrer_employe(self.temporaire, employe('Kyle', 'Munoz', 'A', '01-18', 'kylemunoz.com', 'mOtdep4sse3', ' '))
        with self.assertRaises(ValueError):
            enregistrer_employe(self.temporaire, employe('Mary', 'Moris', 'J', '01-19', 'merymoris@limoilu.com', 'mOtdep4sse3', 0))

        # Asegura que no se pueda agregar empleados con contraseñas inseguras
        with self.assertRaises(ValueError):
            enregistrer_employe(self.temporaire, employe('Johanna', 'Harris', 'F', '05-20', 'jharris@limoilu.com', 'mOtdep4sse3', 'mOtdep4sse3'))

        # Asegura que no se puedan agregar empleados con correos electrónicos duplicados
        with self.assertRaises(ValueError):
            enregistrer_employe(self.temporaire, employe('Mark', 'McGwire', 'M', '01-22', 'markmcgwire@gmail.com', 'mOtdep4sse3', '0'))
            enregistrer_employe(self.temporaire, employe('Sam', 'Sosa', 'M', '01-24', 'markmcgwire@gmail.com', 'mOtdep4sse3', '1'))

    def test_authentifier_employe(self):

         # Ajouter des employés pour les tests
        self.temporaire = enregistrer_employe(self.temporaire, employe('Julian', 'Munoz', 'M', '01-01', 'julianemail@limoilu.com', 'motdEpasse1', '1'))
        self.temporaire = enregistrer_employe(self.temporaire, employe('Sebastien', 'Bustamante', 'M', '01-03', 'julianemail3@limoilu.com', 'mOtdep4sse', '0'))

        # Teste l'authentification d'un employé existant et valide
        employe_auth = authentifier_employe(self.temporaire, 'julianemail@limoilu.com', 'motdEpasse1')
        self.assertIsNotNone(employe_auth)
        self.assertIsInstance(employe_auth, employe)

        # Teste l'authentification d'un employé existant mais avec un mot de passe invalide
        with self.assertRaises(ValueError):
            authentifier_employe(self.temporaire, 'julianemail@limoilu.com', 'motdEpasse')

        # Teste l'authentification d'un employé inexistant
        with self.assertRaises(ValueError):
            authentifier_employe(self.temporaire, 'inconnu@limoilu.com', 'motdepasse')

    def test_enregistrer_carte(self):

        # Ajouter un client pour les tests
        self.temporaire = enregistrer_client(self.temporaire, client('Alice', 'Dupont', 'F', 'alice@limoilu.com', 'Motdepasse1'))

        # Teste l'ajout d'une carte de crédit pour un client existant
        self.assertTrue(enregistrer_carte(self.temporaire, 'alice@limoilu.com', '1111222233334444', '12-25'))

        # Teste l'ajout d'une carte de crédit pour un client inexistant
        with self.assertRaises(ValueError):
            enregistrer_carte(self.temporaire, 'inconnu@limoilu.com', '1111222233334444', '12-25')

        # Teste l'ajout d'une carte de crédit avec un champ manquant
        with self.assertRaises(ValueError):
            enregistrer_carte(self.temporaire, 'alice@limoilu.com', '', '12-25')

        # Teste l'ajout d'une carte de crédit avec une date d'expiration invalide
        with self.assertRaises(ValueError):
            enregistrer_carte(self.temporaire, 'alice@limoilu.com', '1111222233334444', '13-25')

        # Teste l'ajout d'une carte de crédit expirée
        with self.assertRaises(ValueError):
            enregistrer_carte(self.temporaire, 'alice@limoilu.com', '1111222233334444', '01-21')

    def test_ajouter_acteur(self):
        # Cree l'ajout d'un film
        Film = film("Le Parrain", 1972, "Produit par les studios Paramount, le film est l'adaptation du roman du même nom (1969) écrit par le romancier Mario Puzo. L'histoire se déroule à New York sur une période allant de 1945 à 1955, et raconte les luttes de pouvoir au sein de la mafia américaine new-yorkaise, avec pour protagoniste principal la famille Corleone, l'une des cinq familles mafieuses de la ville, la famille Corleone étant menée par son patriarche, Don Vito Corleone dit le « Parrain » (Marlon Brando), un personnage puissant et influent")
        self.temporaire = enregistrer_film(self.temporaire,Film)
        
        # Teste l'ajout des acteurs aux films
        acteur1 = acteur("Marlon", "Brando", "M", "Don Vito Corleone", "12-85", "", "Paramount")
        acteur2 = acteur("Al", "Pacino", "M", "Michael Corleone", "08-80", "", "Paramount")
        Film = self.temporaire['films'][0]
        Film.ajouter_acteur(acteur1)
        Film.ajouter_acteur(acteur2)
        Film.ajouter_categorie("Viex", "Films tres vieux")
        Film.ajouter_categorie("Mafias", "Films avec contenus de mafias")

        # Teste si retourne un erreur en passant des donnees invalides
        with self.assertRaises(ValueError):
            acteur("Marlon", "Brando", "M", "Don Vito Corleone", "12-55", "gfd", "Paramount")
        with self.assertRaises(ValueError):
            acteur("", "Brando", "R", "Don Vito Corleone", "12-55", "01-12", "Universal")

        # Teste si les acteurs ont ete ajoutes
        self.assertEqual(len(Film.acteurs), 2)
        self.assertIn(acteur1, Film.acteurs)
        self.assertIn(acteur2, Film.acteurs)


