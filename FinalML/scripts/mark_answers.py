from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

def mark_answer(user_answer, generated_answer, question_marks):
    corpus = [user_answer, generated_answer]                                                                                                                                                                                                   
    vect = TfidfVectorizer(min_df=1, stop_words="english")                                                                                                                                                                                                   
    tfidf = vect.fit_transform(corpus)                                                                                                                                                                                                                       
    pairwise_similarity = tfidf * tfidf.T 

    arr = pairwise_similarity.toarray()
    np.fill_diagonal(arr, np.nan)
    marks_got = arr[0][1] * question_marks
    return marks_got