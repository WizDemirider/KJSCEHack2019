from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.utils.html import escape

from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required

from . import models
from FinalML import text_detection, mark_answers
from django.conf import settings


def index(request):
    return redirect('login')

def signupUser(request):
    if request.method == 'POST':
        username = escape(request.POST['username'])
        raw_password = escape(request.POST['password1'])
        raw_password2 = escape(request.POST['password2'])
        try:
            if raw_password == raw_password2 and len(raw_password) >= 6:
                user = User.objects.create(username=username, password=raw_password)
                user.set_password(raw_password)
                user.save()
                login(request, user) # logs User in
                return redirect('home')
            elif len(raw_password) >= 6:
                return render(request, 'Authentication/signup.html', {'error': "Passwords do not match!"})
            else:
                return render(request, 'Authentication/signup.html', {'error': "Password must be 6 characters or more"})
        except Exception as e:
            return render(request, 'Authentication/signup.html', {'error': str(e)})
    return render(request, 'Authentication/signup.html', {'error': None})

def loginUser(request):
    if request.method == 'POST':
        username = escape(request.POST['username'])
        raw_password = escape(request.POST['password'])
        user = authenticate(username=username, password=raw_password)
        if user is not None:
            login(request, user) # logs User in
            return redirect('home')
        else:
            return render(request, 'Authentication/signup.html', {'error': "Unable to Log you in!"})
    return render(request, 'Authentication/login.html', {'error': None})

def logoutUser(request):
    logout(request)
    return redirect('index')

@login_required
def home(request):
    return render(request, 'Main/dashboard.html')

@login_required
def uploadBook(request):
    subjects = models.Subject.objects.all()
    course_subjects = []
    success_message = None
    error_message = None
    for subject in subjects:
        course_subjects.append({'course': subject.course, 'subject': subject})
    if request.method == "POST" and request.FILES:
        book = models.ReferenceBook(
            subject_id=escape(request.POST['subject']),
            description=escape(request.POST['description']),
            uploaded_by=request.user,
        )
        request.FILES['file'].original_filename = request.FILES['file'].name + book.description
        book.file = request.FILES['file']
        book.save()
        success_message = "Saved Successfully!"
    elif request.method == "POST":
        error_message = "No file found!"
    return render(request, 'Main/upload_book.html', context={'course_subjects': course_subjects, 'success_message': success_message, 'error_message': error_message})

@login_required
def uploadQuestion(request):
    subjects = models.Subject.objects.all()
    course_subjects = []
    success_message = None
    error_message = None
    for subject in subjects:
        course_subjects.append({'course': subject.course, 'subject': subject})
    if request.method == "POST" and request.FILES:
        paper = models.QuestionPaper(
            subject_id=escape(request.POST['subject']),
            description=escape(request.POST['description']),
            uploaded_by=request.user,
        )
        request.FILES['file'].original_filename = request.FILES['file'].name + paper.description
        paper.file = request.FILES['file']
        paper.save()
        success_message = "Saved Successfully!"
    elif request.method == "POST":
        error_message = "No file found!"
    return render(request, 'Main/upload_question.html', context={'course_subjects': course_subjects, 'success_message': success_message, 'error_message': error_message})

@login_required
def getSolution(request):
    papers = models.QuestionPaper.objects.all()
    books = models.ReferenceBook.objects.all()
    success_message = None
    error_message = None
    paper_solution = None
    if request.method == "POST":
        paper_id = escape(request.POST['question_paper'])
        book_id = escape(request.POST['book'])
        paper = models.QuestionPaper.objects.get(id=paper_id)
        book = models.ReferenceBook.objects.get(id=book_id)
        questions = models.Question.objects.filter(paper=paper)
        
        if book.subject.id != paper.subject.id:
            error_message = "These are not of the same subject!"
        elif questions.exists():
            paper_solution = []
            for question in questions:
                paper_solution.append((question.question_text, question.correct_answer_text))
        else:
            paper_solution = text_detection.run(book.file.name, paper.file.name)
            success_message = "Solution Generated Successfully!"
            for QnA in paper_solution:
                q = QnA[0]
                if q[-1] == ')':
                    i=1
                    while q[-1-i] != '(':
                        pass
                    if i>1 and i<=3:
                        marks = int(q[-1-i:-1].trim())
                    else:
                        marks = int(len(q)/20)
                else:
                    marks = int(len(q)/20)
                question = models.Question.objects.create(
                    paper=paper,
                    question_text=q,
                    correct_answer_text=QnA[1],
                    answer_found_from=book,
                    marks=marks,
                )

    return render(request, 'Main/get_solution.html', context={'papers': papers, 'books': books, 'paper_solution': paper_solution, 'success_message': success_message, 'error_message': error_message})

@login_required
def correctAnswerSheet(request):
    questions = models.Question.objects.all()
    success_message = None
    error_message = None
    question = None
    answer = None
    if request.method == "POST" and request.FILES:
        answer = models.UserAnswer(
            question=escape(request.POST['question']),
            marks=question.marks,
            uploaded_by=request.user
        )
        question = answer.question
        request.FILES['file'].original_filename = request.FILES['file'].name + str(answer.question.id)
        answer.file = request.FILES['file']
        answer_text = text_detection.get_data(answer.file.name)
        answer.scored_marks = mark_answers.mark_answer(answer_text, question.correct_answer_text, answer.marks)
        answer.save()
        success_message = "Saved Successfully! Generating scores!"
    elif request.method == "POST":
        error_message = "No file found!"
    return render(request, 'Main/correct_answer_sheet.html', context={'questions': questions, 'success_message': success_message, 'error_message': error_message, 'question': question, 'answer': answer})
