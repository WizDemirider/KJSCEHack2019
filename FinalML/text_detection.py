import pdf2image
from PIL import Image
import pytesseract
import os
from fuzzywuzzy import fuzz

from  pdf2image import convert_from_path
from .split_pdf import PDFsplit
from .text_summarization import text_summarize
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

def get_data(filepath):
    pages = convert_from_path(filepath)
    data = ''
    num = 0
    page_num = 0

    for page in pages:
        if page_num > 10:
            break
        page_num += 1
    
        name = "out.jpg"
        page.save(name, 'JPEG')
        data += '\n\n\n\n' + pytesseract.image_to_string(Image.open('out.jpg'), lang='eng')

        os.remove(name)
    return data

def get_questions(paper):

    questions = []

    questions.append(get_data(paper))

    questions = [x.split('\n') for x in questions if x != '']

    questions = [l for x in questions for l in x]

    question_w_keywords = []

    keywords = [
        'explain', 
        'what', 
        'how', 
        'why', 
        'write', 
        'classify', 
        'differentiate',
        'short note',
        'compare', 
        'where',
        'prove', 
        'who', 
        '(a)',
        '(b)',
        '(c)',
        '(d)',
        '(e)'
    ]

    for sentence in questions:
        for keyword in keywords:
            if keyword in ' '.join([x.lower() for x in sentence.split()]):
                question_w_keywords.append((' '.join([x.lower() for x in sentence.split()]), keyword))

    question_w_keywords = [x[0][x[0].index(x[1]):].capitalize() for x in question_w_keywords]

    qk = []

    for q_index in range(len(question_w_keywords)):
        if q_index < len(question_w_keywords)-1 and question_w_keywords[q_index+1][:3] == '(a)':
            short_note = question_w_keywords[q_index]
        elif question_w_keywords[q_index][:3] == '(a)':
            short_note += ' ' + question_w_keywords[q_index]
        elif question_w_keywords[q_index][:3] in ['(b)', '(c)', '(d)']:
            short_note += ' ' + question_w_keywords[q_index]
        elif question_w_keywords[q_index][:3] == '(e)':
            short_note += question_w_keywords[q_index]
            qk.append(short_note)
            short_note = ''
        else:
            qk.append(question_w_keywords[q_index])

    question_w_keywords = qk

    return question_w_keywords

def get_question_keywords(papers):
    question_w_keywords = get_questions(papers)
    question_w_keywords = [extract_keywords(x) for x in question_w_keywords]
    return question_w_keywords

def get_indices(reference_text, papers):
    qk = get_question_keywords(papers)
    q = get_questions(papers)

    qk = [(x, y) for x, y in zip(q, qk)]

    with open(reference_text, 'r') as file:
        file_lines = file.readlines()
        keyword_index = []
        for k, keyword_arg in qk:
            max_thresh = 30
            max_thresh_line = None
            for line in file_lines:
                fr = fuzz.ratio(line, keyword_arg)
                if fr >= max_thresh:
                    max_thresh = fr
                    max_thresh_line = line
            if max_thresh_line is not None: 
                try:
                    keyword_index.append((k, int(max_thresh_line.split(',')[1][:-2].strip())))
                except:
                    continue
        return (keyword_index)

def run(bookpath, paperpath):
    bookname = bookpath.split('/')[-1]
    indexpath = 'files/indices/'+bookname
    textpath = 'files/text/'+bookname
    if not os.path.exists(indexpath):
        PDFsplit(bookpath, indexpath, 0)
        data = get_data(indexpath)
        with open(textpath, 'w') as file:
            file.write(data)

    question_indices = get_indices(textpath, paperpath)
    question_answers = []
    for question, q_index in question_indices:

        PDFsplit(bookpath, 'files/temp/temp.pdf', q_index+20)
        data = get_data('files/temp/temp.pdf')
        question_answers.append((question, text_summarize(data)))
    return question_answers

if __name__ == '__main__':
    # data = get_data('CN_Index.pdf')
    run()
'''
    Flow: 
        1. Convert the book into a small pdf of 20 pages with the index
        2. Use the get_data function on the pdf of the index 
        3. Get the question paper (can be uploaded)
        4. Get the index of the possible pages (question, index)
        5. Use the indices to create small pdfs by using splitpdf
        6. Then we'll call get_data on those small pdfs
        7. Then we use text summarization to get a concise answer
'''