# tri par selection

l = (5, 8, 10, 2, 1)

# (1, 5, 8, 10, 2)
# sorted / unsorted
# 1, 2, 5, 8, 10
index = 0
#unsorted_index = 0
for unsorted_index in range(0, len(l)-1):
    min = l[unsorted_index]
    min_index = unsorted_index
    for i in range(unsorted_index+1, len(l)):
        if l[i] < min:
            min = l[i]
            min_index = i
    l[min_index] = l[unsorted_index]
    l[unsorted_index] = min

#l.sort()

print("SORTED: ",l)