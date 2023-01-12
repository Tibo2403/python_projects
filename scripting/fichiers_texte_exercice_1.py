# nombres.txt

f = open("nombre.txt","w")

for i in range(10):
    #print(i)
    f.write((str(i+1)))
    f.write("\n")

f.close()