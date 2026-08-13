# Text Preprocessing

Before text can be indexed or matched against a query, it goes through a
normalization pipeline. This project experiments with each step
independently under `search-engine/information-retrieval/`.

## Tokenization

Splitting a sentence into individual words. `lemmatization_tokenization.py`
uses NLTK's `word_tokenize`:

```python
sentence = "the bats were hanging by their feet"
tokenized_words = nltk.word_tokenize(sentence)
# ['the', 'bats', 'were', 'hanging', 'by', 'their', 'feet']
```

## Normalization

- **Lowercasing:** e.g. `"TÌM KIẾM"` → `"tìm kiếm"`.
- **Lemmatization:** reduce a word to its dictionary form using
  `WordNetLemmatizer` (`lemmatization_tokenization.py`):

  ```python
  lemmatizer = WordNetLemmatizer()
  lemmatizer_words = [lemmatizer.lemmatize(word) for word in tokenized_words]
  ```

- **Stemming:** reduce a word to its root form using the Porter stemming
  algorithm (`stemming.py`):

  ```python
  stemmer = PorterStemmer()
  words = ['jumps', 'jumped', 'jumping']
  stemmer_words = [stemmer.stem(word) for word in words]
  # jumps -> jump, jumped -> jump, jumping -> jump
  ```

- **Special-phrase merging:** compound terms are joined so they are treated
  as a single token, e.g. `"ma túy"` → `"ma_túy"`.

## Stop-word removal

Common words that carry little search value (`"và"`, `"của"`, `"là"` /
"and", "of", "is") are filtered out. `stopwords_remove.py` demonstrates this
for English using NLTK's stopword corpus:

```python
stop_words = set(stopwords.words('english'))
words = word_tokenize(text)
filtered_words = [word for word in words if word.lower() not in stop_words]
```

## Where this fits in the pipeline

These steps are applied twice in the proposed architecture (see
[`architecture.md`](./architecture.md)):

- By the **Index Worker**, when building the Inverted Index Storage from
  the source documents.
- By **Query Processing**, when normalizing a user's query before looking it
  up in the inverted index — so that a query and a document use the same
  normalized vocabulary.
