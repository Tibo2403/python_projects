# FICHIERS TEXTE
#
# ouvrir (open) <- nom du fichier, mode
# ecrire (write) / lire (read)
# fermer (close)

import os.path
#dir = "toto"
#if not os.path.exists(dir):
#   os.mkdir(dir)

rep = "C:\\Users\\User\\PycharmProjects\\pythonProject\\scripting\\"
filename = os.path.join(rep,"nom_fichier.txt")
print("filename: " + filename)
if os.path.exists(filename):
    print("Le fichier existe")
    f = open(filename,"r")
    texte = f.read()
    print(texte)
    f.close()
else:
    print("Le fichier n'existe pas")

if os.path.exists(filename):
    os.remove(filename)