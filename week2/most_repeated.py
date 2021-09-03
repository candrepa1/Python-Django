from file import File
import re


class MostRepeated(File):

    def ten_most_repeated_words(self):
        words_total = {}
        words = self.file.read()
        no_punctuation = re.sub("[^\w\s]", "", words)
        words_arr = no_punctuation.split()
        final_format = [element.lower() for element in words_arr]
        for word in final_format:
            words_total[word] = words_total.get(word, 0) + 1
        sorted_total = sorted(words_total.items(), key=lambda x: x[1], reverse=True)
        top_10 = sorted_total[0:10]
        return top_10


if __name__ == '__main__':
    file = MostRepeated()
    file.read_filename("text.txt")
    file.open_file()
    print(file.ten_most_repeated_words())
