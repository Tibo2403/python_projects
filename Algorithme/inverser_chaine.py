# inverser une chaine de caractères

def reverse_string1(str):
    r = ""
    for c in str:
        r = c + r
    return r

def reverse_string2(str):
    return str[::-1]

# s[i] = s(len(s)-1)
s = "Bonjour toto"
print(reverse_string1(s))
print(s[::-1])