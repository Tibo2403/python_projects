import turtle

#escalier(taile, nb)

def escalier(taille, nb):
    for i in range(0,nb):
        t.forward(taille)
        t.left(90)
        t.forward(taille)
        t.right(90)
        #taille -= 10
    t.forward(taille)

t = turtle.Turtle()

# 5 marches de 30 pixels
escalier(50, 10)
turtle.done()