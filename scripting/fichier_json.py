# JSON
# Manipuler des données structurées

import json

# Personne
#   nom : str
#   age : int
#   amis : [str]

# Paul
# 25
# Sophie, Marie, Jean
# Pierre
# 18
# Eric, Marc

personne = {"nom" : "Paul",
            "age" : 25,
            "amis": ["Sophie", "Marie", "Jean"]}
# Sérialiser DATA -> TXT "" (json) dumps
# Désérialiser TXT (json) -> DATA loads

personne_json = json.dumps(personne)

f = open("fichier_json.txt", "w")
donnees_json = f.read()
json.loads(donnees_json)
f.close()

print("Nom:" + personne["nom"])