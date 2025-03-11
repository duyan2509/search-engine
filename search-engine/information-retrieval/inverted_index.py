import json
class InvertedIndex:
    def __init__(self):
        self.inverted_index = {}
    def add_to_index(self, doc_id, doc):
      terms = doc.split()
      for position, term in enumerate(terms):
          if term not in self.inverted_index:
              self.inverted_index[term] = {}
          if doc_id not in self.inverted_index[term]:
              self.inverted_index[term][doc_id] = []
          self.inverted_index[term][doc_id].append(position)
    def search(self, query):
        terms = query.split()
        results = None
        for term in terms:
            if term in self.inverted_index:
                if results is None:
                    results = set(self.inverted_index[term].keys())
                else:
                    results.intersection_update(self.inverted_index[term].keys())
        if results is None:
            return []
        else:
            search_results = []
            for doc_id in results:
                positions =[self.inverted_index[term][doc_id] for term in terms]
                search_results.append((doc_id, positions))
            return search_results
index = InvertedIndex()

index.add_to_index(1, "banana apple apple")
index.add_to_index(2, "banana cherry")
index.add_to_index(3, "apple  cherry")

print(json.dumps(index.inverted_index, indent=2))

query = "apple"

search_results = index.search(query)
print(f"Search results for {query}:")
if search_results==[]:
    print("No results found.")
for doc_id, positions in search_results:
    print(f"Document ID: {doc_id}")
    print(f"Positions: {positions}")