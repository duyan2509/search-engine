import math

corpus ={
    'doc1': 'the quick brown fox',
    'doc2': 'jumped over the lazy dog',
    'doc3': 'the quick brown dog jumped over the lazy fox',
    'doc4': 'the lazy dog slept'
}

def tokenize(doc):
    return doc.split()

def tfidf(term,doc):
    tf = doc.count(term)/len(tokenize(doc))
    idf = math.log(len(corpus)/ sum (1 for doc in corpus.values() if term in tokenize(doc)))
    return tf*idf

def tfidf_vector(doc):
    vector = {}
    for term in tokenize(doc):
        vector[term] = tfidf(term,doc)
    return vector

vector = {}

for doc_id, doc in corpus.items():
    vector[doc_id] = tfidf_vector(doc)

def cosine_similarity(vector1, vector2):
    dot_product = sum(vector1.get(term,0)*vector2.get(term,0) for term in set(vector1) & set(vector2))
    norm1 = math.sqrt(sum((val**2 for val in vector1.values())))
    norm2 = math.sqrt(sum((val**2 for val in vector2.values())))
    return dot_product / (norm1 * norm2)

def vector_space_retrieval(query):
    query_vector = tfidf_vector(query)
    results = []
    for doc_id, doc_vector in vector.items():
        score = cosine_similarity(query_vector, doc_vector)
        results.append((doc_id, score))
    results.sort(key=lambda x: x[1], reverse=True)
    return results

query = 'quick brown fox'
results = vector_space_retrieval(query)
print(f"Results for query: {query}")
for doc_id, score in results:
    print(f"Document ID: {doc_id}, Score: {score}")