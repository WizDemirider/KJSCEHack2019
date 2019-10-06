from django.db import models
from django.contrib.auth.models import User

class Course(models.Model):
    course_name = models.CharField(max_length=100)

    def __str__(self):
        return self.course_name


class Subject(models.Model):
    subject_name = models.CharField(max_length=100)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.course) + ' - ' + self.subject_name

class ReferenceBook(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to="files/books/")
    description = models.CharField(max_length=200)
    uploaded_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return str(self.subject) + ' ' + self.description

class QuestionPaper(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to="files/question_papers/")
    description = models.TextField()
    uploaded_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.description + ' ' + str(self.subject)

class Question(models.Model):
    paper = models.ForeignKey(QuestionPaper, null=True, on_delete=models.CASCADE)
    question_text = models.TextField()
    correct_answer_text = models.TextField(null=True, default=None)
    answer_found_from = models.ForeignKey(ReferenceBook, null=True, on_delete=models.SET_NULL)
    marks = models.IntegerField(default=0)

    def __str__(self):
        return self.question_text
        

class UserAnswer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.PROTECT)
    answer_text = models.TextField()
    marks = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to="files/answers/")
    scored_marks = models.IntegerField(default=0)
    uploaded_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return str(self.question) + ' ' + str(self.answer_sheet)
