import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

nltk.download('stopwords')
nltk.download('punkt_tab')

text = "This is an example sentence demonstrating the removal of stopwords."

stop_words = set(stopwords.words('english'))

words = word_tokenize(text)

filtered_words = [word for word in words if word.lower() not in stop_words]

filtered_text = " ".join(filtered_words)

print("Original Text: ", text)
print("After stopword removal: ", filtered_text)