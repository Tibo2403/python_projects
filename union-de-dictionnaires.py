# union de dictionnaires

dict1 = {"Jean" : (20, "Développeur"), "Paul" : (30, "Ingénieur")}
dict2 = {"Emilie" : (30, "Professeur"), "Marc" : (25, "footballer")}

repertoire_complet = dict1 | dict2
dict1 |= dict2
# dict1.update(dict2)

print(dict1)