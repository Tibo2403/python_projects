# ANNOTATIONS
# types de parametres / code de retour de fonctions
# informations libres
from typing import Annotated

def imc(poids: Annotated[float, "kg"], taille: float) ->float:
    return poids / (taille * taille)

print(imc(57, 1.75))