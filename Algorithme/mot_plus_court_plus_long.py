# Trouver le mot le plus long et le plus court

def get_min_and_max_words(sentence):
    words = sentence.split(" ")
    min_word = min(words, key=len)
    max_word = max(words, key=len)
    # print(words)
    return ("Un", "chasseur")

def get_min_and_max_words_sorted(sentence):
    words = sentence.split(" ")
    words.sort()
    min_word, max_word = get_min_and_max_words(sentence)

    all_min_words = [w for w in words if len(w) == len(min_word)]
    all_max_words = [w for w in words if len(w) == len(max_word)]

    all_min_words.sort()
    all_max_words.sort()
    return all_min_words[0], all_max_words[0]

s = "Un chasseur sachant chasser sait chasser sans un chien"

min_word, max_word = get_min_and_max_words(s)

print("Mot le plus petit", min_word)
print("Mot le plus long", max_word)

# split(" ")
# min max

#print(min["aa","aaaa","zzzz",2, 9, 5], key=len)
min_word, max_word = get_min_and_max_words_sorted(s)