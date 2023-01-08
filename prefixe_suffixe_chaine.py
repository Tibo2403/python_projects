phrase = "jean a mangé un gateau"

#print(phrase.strip("gateau"))
print(phrase.removesuffix("gateau"))
print(phrase.removeprefix("jean").removesuffix("gateau"))
