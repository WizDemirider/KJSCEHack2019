from rake_nltk import Rake

def extract_keywords(text):
    r = Rake()
    r.extract_keywords_from_text(text)
    keywords_dict_scores = r.get_word_degrees()
    keywords = list(keywords_dict_scores.keys())
    keywordString = ""
    for keyword in keywords:
        keywordString = keywordString + " " + keyword
    keywordString = keywordString.lstrip()
    return keywordString

if __name__ == '__main__':
    text = "What is error detection and correction?"
    print(extract_keywords(text))
