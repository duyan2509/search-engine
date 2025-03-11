import nltk
from nltk.stem import PorterStemmer
stemmer = PorterStemmer()
words = ['jumps','jumped','jumping']
stemmer_words = [stemmer.stem(word) for word in words]

for i in range(len(words)):
    print(f"{words[i]} -> {stemmer_words[i]}")