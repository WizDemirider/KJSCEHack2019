from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.utils.html import escape

from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required

from . import models


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
    return render(request, 'Main/get_solution.html')


@login_required
def correctAnswerSheet(request):
    papers = models.QuestionPaper.objects.all()
    success_message = None
    error_message = None
    if request.method == "POST" and request.FILES:
        answer_sheet = models.UserAnswerSheet(
            question_paper_id=escape(request.POST['question_paper']),
            description=escape(request.POST['description']),
            uploaded_by=request.user,
        )
        request.FILES['file'].original_filename = request.FILES['file'].name + answer_sheet.description
        answer_sheet.file = request.FILES['file']
        answer_sheet.save()
        success_message = "Saved Successfully! Generating scores!"
    elif request.method == "POST":
        error_message = "No file found!"
    return render(request, 'Main/correct_answer_sheet.html', context={'papers': papers, 'success_message': success_message, 'error_message': error_message})
