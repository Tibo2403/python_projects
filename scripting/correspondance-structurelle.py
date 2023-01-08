# CORRESPONDANCE STRUCTURELLE
# (Structural pattern matching)

# switch case -> match case

phrase = input("Parlez moi : ")
if phrase == "Bonjour" or phrase == "hello" or phrase == "salut!":
    print("Bonjour, comment allez-vous ?")
elif phrase == "Bien":
    print("Je vais bien aussi")
elif phrase == "Bye":
    print("Au revoir")
else:
    print("Je n'ai pas compris")

# #wildcard
# while True:
#     phrase = input("Parlez moi ! ")
#     match phrase:
#         case "Bonjour":
#             print("Bonjour, comment allez-vous ?")
#         case "bien":
#             print("Je vais bien aussi")
#         case "bye":
#             print("Au revoir")
#             break
#         case _:
#             print("Je n'ai pas compris")

personne1 = {"nom": "Paul", "infos" : (30, "Ingenieur informatique")}
personne2 = {"nom": "Marc", "age": 20}

personnes = {personne1, personne2}

# for personne in personnes:
#     match personne:
#         case {"nom": nom, "infos" :(age, metier)}:
#             print(f"{nom},{age} ans, {metier}")
#         case _:
#             print("format non supporté")