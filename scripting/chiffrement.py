alphabet = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U",
            "V", "W", "X", "Y", "Z", 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p',
            'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', "'", "ù", "é", "è", "à", "ç", "-", "ê", " "]


# Calcul du pgcd de a et b
def pgcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a


# fonction de chiffrement affine
def chiffrementAffine(a, b, L):
    x = alphabet.index(L)
    y = (a * x + b) % len(alphabet)
    return alphabet[y]


# Calcul de l'inverse d'un nombre modulo 26
def inverse(a):
    x = 0
    while (a * x % len(alphabet) != 1):
        x = x + 1
    return x


# Fonction de déchiffrement
def dechiffrementAffine(a, b, L):
    x = alphabet.index(L)
    y = (inverse(a) * (x - b)) % len(alphabet)
    return alphabet[y]


# Affichage du mot chiffré
def crypt(M, a, b):
    if (pgcd(a, len(alphabet)) == 1):
        mot = [chiffrementAffine(a, b, i) for i in M]
        return "".join(mot)
    else:
        return "Chiffrement impossible. Veuillez choisir un nombre a premier avec" + str(len(alphabet)) + "."


# Affichage du mot déchiffré
def decrypt(M, a, b):
    if (pgcd(a, len(alphabet)) == 1):
        mot = [dechiffrementAffine(a, b, i) for i in M]
        return "".join(mot)
    else:
        return "Déchiffrement impossible. Le nombre a n'est pas premier avec" + str(len(alphabet)) + "."


# Menu
def menu():
    print('Menu du jour...\n----------------')
    print('1. Chiffrer un message')
    print('2. Déchiffrer un message\n-----------------------\n')
    choix = int(input('Quel est votre choix ? '))
    if choix == 1:
        chiffrer()
    elif choix == 2:
        dechiffrer()
    else:
        print('Can you be serious please... ?\n')
        menu()


# Retour au menu ?
def return_menu():
    rep = input('\nSouhaitez-vous revenir au menu (O/N) ? ')
    if rep.upper() == 'N':
        the_end()
    elif rep.upper() == 'O':
        menu()
    else:
        print('Can you be serious please... ?\n')
        return_menu()


# the_end()
def the_end():
    print("Ok. C'est vous qui voyez... See you soon !")


# chiffrer
def chiffrer():
    msg = input('Entrez le message à chiffrer : ')
    a = int(input('Entrez la première clé : '))
    b = int(input('Entrez la seconde clé : '))
    print('Le chiffrement donne : ', crypt(msg, a, b))
    return_menu()


def dechiffrer():
    msg = input('Entrez le message à déchiffrer : ')
    a = int(input('Entrez la première clé : '))
    b = int(input('Entrez la seconde clé : '))
    print('Le chiffrement donne : ', decrypt(msg, a, b))
    return_menu()


menu()