import re


def get_input():
    filename = input("Filename: ")
    try:
        return repeated_words(filename)
    except FileNotFoundError:
        return "File not found"
    # "text.txt"


def repeated_words(filename):
    words_total = {}
    file = open(filename)
    words = file.read()
    no_punctuation = re.sub("[^\w\s]", "", words)
    words_arr = no_punctuation.split()
    final_format = [element.lower() for element in words_arr]
    for word in final_format:
        words_total[word] = words_total.get(word, 0) + 1
    sorted_total = sorted(words_total.items(), key=lambda x: x[1], reverse=True)
    top_10 = sorted_total[0:10]
    return top_10


print(get_input())
