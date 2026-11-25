# FAIRE DES APPELS RÉSEAU AVEC REQUESTS
#
# https://codeavecjonathan.com/res/programmation.txt
# https://codeavecjonathan.com/res/pizzas1.json
# https://codeavecjonathan.com/res/exemple.html

import requests

# API REST
"""reponse = requests.get("https://codeavecjonathan.com/res/pizzas1.json", timeout=10)
if reponse.status_code == 200:
    reponse.encoding = "utf-8"
    print(reponse.text)
    pizzas = json.loads(reponse.text)
    print("Nombre de pizzas :", len(pizzas))
else:
    print("ERREUR code : " + str(reponse.status_code))"""

reponse = requests.get("https://codeavecjonathan.com/res/exemple.html", timeout=10)
if reponse.status_code == 200:
    reponse.encoding = "utf-8"
    print(reponse.text)
else:
    print("ERREUR code : " + str(reponse.status_code))