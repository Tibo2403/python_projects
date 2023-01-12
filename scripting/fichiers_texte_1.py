# FICHIERS TEXTE
#
# ouvrir (open) <- nom du fichier, mode
# ecrire (write) / lire (read)
# fermer (close)

f = open("nom_fichier.txt", "w")

#f.write("Bonjour")
l = ["premiere phrase\n", "deuxieme phrase\n", "troisieme phrase\n"]

f.write("\n".join())
f.write("\nFin")
f.writelines(l)
f.close()