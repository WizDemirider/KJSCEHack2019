import numpy as np
import pandas as pd
import nltk
import re
from nltk.tokenize import sent_tokenize

text = "Maria Sharapova has basically no friends as tennis players on the WTA Tour. The Russian player has no problems in openly speaking about it and in a recent interview she said: 'I don't really hide any feelings too much. I think everyone knows this is my job here. When I'm on the courts or when I'm on the court playing, I'm a competitor and I want to beat every single person whether they're in the locker room or across the net... BASEL, Switzerland (AP), Roger Federer advanced to the 14th Swiss Indoors final of his career by beating seventh-seeded Daniil Medvedev 6-1, 6-4 on Saturday. Seeking a ninth title at his hometown event, and a 99th overall, Federer will play 93th-ranked Marius Copil on Sunday. Federer dominated the 20th-ranked Medvedev and had his first match-point chance to break serve again at 5-1... Roger Federer has revealed that organisers of the re-launched and condensed Davis Cup gave him three days to decide if he would commit to the controversial competition. Speaking at the Swiss Indoors tournament where he will play in Sundays final against Romanian qualifier Marius Copil, the world number three said that given the impossibly short time frame to make a decision, he opted out of any commitment..."
sentences = sent_tokenize(text)
# sentences = [y for x in sentences for y in x]

clean_sentences = pd.Series(sentences).str.replace("[^a-zA-Z]", " ")
clean_sentences = [s.lower() for s in clean_sentences]

from nltk.corpus import stopwords
stop_words = stopwords.words('english')

def remove_stopwords(sen):
    sen_new = " ".join([i for i in sen if i not in stop_words])
    return sen_new

clean_sentences = [remove_stopwords(r.split()) for r in clean_sentences]

# word_embeddings = {}
# f = open('glove.6B.100d.txt', encoding='utf-8')
# for line in f:
#     values = line.split()
#     word = values[0]
#     coefs = np.asarray(values[1:], dtype='float32')
#     word_embeddings[word] = coefs
# f.close()

# sentence_vectors = []
# for i in clean_sentences:
#   if len(i) != 0:
#     v = sum([word_embeddings.get(w, np.zeros((100,))) for w in i.split()])/(len(i.split())+0.001)
#   else:
#     v = np.zeros((100,))
#   sentence_vectors.append(v)

# sim_mat = np.zeros([len(sentences), len(sentences)])

# from sklearn.metrics.pairwise import cosine_similarity
# for i in range(len(sentences)):
#   for j in range(len(sentences)):
#     if i != j:
#       sim_mat[i][j] = cosine_similarity(sentence_vectors[i].reshape(1,100), sentence_vectors[j].reshape(1,100))[0,0]

# import networkx as nx

# nx_graph = nx.from_numpy_array(sim_mat)
# scores = nx.pagerank(nx_graph)

# ranked_sentences = sorted(((scores[i],s) for i,s in enumerate(sentences)), reverse=True)

# for i in range(10):
#   print(ranked_sentences[i][1])