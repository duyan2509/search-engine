import nltk
from nltk.stem import WordNetLemmatizer
#Tokenization
sentence = "the bats were hanging by their feet"
tokenized_words = nltk.word_tokenize(sentence)
print(f"Tokenized words: {tokenized_words}")
lemmatizer = WordNetLemmatizer()
lemmatizer_words=[lemmatizer.lemmatize(word) for word in tokenized_words]
print(f"Lemmatized words: {lemmatizer_words}")