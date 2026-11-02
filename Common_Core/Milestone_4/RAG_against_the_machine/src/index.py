from rank_bm25 import BM25Okapi

# Tokenizar os teus chunks
tokenized_corpus = [doc.lower().split() for doc in chunks]
bm25 = BM25Okapi(tokenized_corpus)

# Pesquisar
tokenized_query = query.lower().split()
top_scores = bm25.get_top_n(tokenized_query, chunks, n=k)