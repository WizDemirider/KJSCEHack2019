import pdf2image
from PIL import Image
import pytesseract
import os

from  pdf2image import convert_from_path

def get_data(filepath, foldername='', remove=True):
    pages = convert_from_path(filepath)

    data = ''

    num = 0

    page_num = 0

    print(len(pages))

    for page in pages:
        if page_num > 10:
            break
        page_num += 1
        if foldername:
            try:
                os.mkdir(foldername)
            except:
                pass

            name = f"{foldername}/out{num}.jpg"
            page.save(name, 'JPEG')
            data += '\n\nPageBreak\n\n' + pytesseract.image_to_string(Image.open(f'{foldername}/out{num}.jpg'), lang='eng')
            num += 1
        
        else:
            name = f"out.jpg"
            page.save(name, 'JPEG')
            data += '\n\nPageBreak\n\n' + pytesseract.image_to_string(Image.open('out.jpg'), lang='eng')

        if remove:
            os.remove(name)
    return data

def get_questions(subject_name):

    questions = []

    for i in range(1, 5):
        questions.append(get_data(f'{subject_name}/{i}.pdf'))

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
        'who', 
        'short note',
        'compare', 
        'where',
        'prove',
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



if __name__ == '__main__':
    # print(get_questions('CN_Papers'))
    data = get_data('CN_Techmax.pdf')
    with open('cn_text.txt', 'w') as file:
        file.write(data)