from Bio import Entrez
Entrez.email = "Thibault.ahn@gmail.com"
req_esearch = Entrez.esearch(db="pubmed", term="transferrin")
res_esearch = Entrez.read(req_esearch)
res_esearch.keys()
res_esearch["IdList"]
import matplotlib.pyplot as plt

temps = [1, 2, 3, 4, 6, 7, 9]
concentration = [5.5, 7.2, 11.8, 13.6, 19.1, 21.7, 29.4]
plt.scatter(temps, concentration, marker="o", color="blue")
plt.xlabel("Temps (h)")
plt.ylabel("Concentration (mg/L)")
plt.title("Concentration de produit en fonction du temps")
plt.show()

import numpy as np
import matplotlib.pyplot as plt

temps = [1, 2, 3, 4, 6, 7, 9]
concentration = [5.5, 7.2, 11.8, 13.6, 19.1, 21.7, 29.4]
plt.scatter(temps, concentration, marker="o", color = "blue")
plt.xlabel("Temps (h)")
plt.ylabel("Concentration (mg/L)")
plt.title("Concentration de produit en fonction du temps")
x = np.linspace(min(temps), max(temps), 50)
y = 2 + 3 * x
plt.plot(x, y, color='green', ls="--")
plt.grid()
plt.savefig("concentration_vs_temps.png", bbox_inches='tight', dpi=200)

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

sequence = "ACGATCATAGCGAGCTACGTAGAA"
bases = ["A", "C", "G", "T"]
distribution = []
for base in bases:
    distribution.append(sequence.count(base))

x = np.arange(len(bases))
plt.bar(x, distribution)
plt.xticks(x, bases)
plt.xlabel("Bases")
plt.ylabel("Nombre")
plt.title(f"Distribution des bases\n dans la séquence {sequence}")
plt.savefig("distribution_bases.png", bbox_inches="tight", dpi=200)
data = {"a": np.arange(10, 40, 10),
        "b": np.arange(11, 40, 10),
        "c": np.arange(12, 40, 10),
        "d": np.arange(13, 40, 10)}
df = pd.DataFrame(data)
df.index = ["chat", "singe", "souris"]
df

def plot_phosphores_3d(X, Y, Z, x, y, z):
    """Graphe 3D des phosphores.

    X, Y, Z : arrays 1D des coordonnées des P de la monocouche upper.
    x, y, z : floats, coordonnées du centre de masse (COM) de la upper.
    """
    # Init plot.
    import matplotlib.pyplot as plt
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    # X, Y et Z sont des arrays 1D de n éléments (par exemple X représente tous les x des P de la monocouche upper).
    ax.scatter(X, Y, Z, c="salmon", marker="o")
    # x, y, z sont des floats avec les coordonnées du COM de la upper.
    ax.scatter(x, y, z, c="red", marker="x")
    # Axis + title.
    ax.set_xlabel("x (Å)")
    ax.set_ylabel("y (Å)")
    ax.set_zlabel("z (Å)")
    ax.set_title("Graphe 3D des phosphores")
    plt.show()
