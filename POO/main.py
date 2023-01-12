# Personne (entité -> class)
#   Données : nom, age
#   Actions : (methodes)
#       - SePresenter()
#       - DemanderNom() / input
# [Personne "Jean"]     [Personne "Paul"]

# --------------------- Definition -------------------
class Personne:
        def __int__(self, nom):
            self.nom = nom
            print("Constructeur Personne "+nom)

        def SePresenter(self):
            print("Bonjour, je m'appelle toto")

# --------------------- Utilisation ------------------
personne1 = Personne() # Je crée une personne
Personne.SePresenter("Jean")

# personne2 = Personne()
personne1.SePresenter("Jean")

# def demander_age():
#     age_int = 0
#     while age_int == 0:
#         age_str = input("Quel est votre age ?")
#         try:
#             age_int = int(age_str)
#         except:
#             print("ERREUR: Vous devez rentrer un nombbre pour l'age")
#     return age_int
#
# #demander le nom
# nom = ""
# while nom == "":
#     nom = input("Quel est votre nom ?")
#
# #demander l'age
# age = demander_age()
# print("Vous vous appelez " + nom + ", vous avez " + str(age) + " ans.")
# print("L'an prochain vous aurez " + str(age+1) + " ans.")
