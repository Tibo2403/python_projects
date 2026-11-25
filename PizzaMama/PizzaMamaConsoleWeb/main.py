import requests
import json

url = "https://jrpizzamamadjango2.herokuapp.com/api/GetPizzas"

data = requests.get(url, timeout=10)

# print(data.text)

pizzas = json.loads(data.text)
# print(pizzas)
# print(len(pizzas))

print("Liste des pizzas :")

for pizzaModel in pizzas:
    pizza = pizzaModel['fields']
    print(pizza['nom'] + " : " + str(pizza['prix']) + "€")




