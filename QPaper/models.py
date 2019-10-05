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
        return str(self.course) + self.subject_name

class ReferenceBook(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to="files/books/")
    date = models.DateField(null=True)
    description = models.CharField(max_length=200)
    uploaded_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.description + str(self.subject)

class QuestionPaper(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to="files/question_papers/")
    date = models.DateField(null=True)
    description = models.TextField()
    uploaded_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    total_marks = models.IntegerField()

    def __str__(self):
        return self.description + str(self.subject) + self.date

class Question(models.Model):
    paper = models.ForeignKey(QuestionPaper, null=True, on_delete=models.CASCADE)
    question_text = models.TextField()
    correct_answer_text = models.TextField(null=True, default=None)
    answer_found_from = models.ForeignKey(ReferenceBook, null=True, on_delete=models.SET_NULL)
    marks = models.IntegerField(default=0)

    def __str__(self):
        return self.question_text

class UserAnswerSheet(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to="files/answer_papers/")
    date = models.DateField(null=True)
    description = models.TextField()
    uploaded_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    total_marks = models.IntegerField(default=0)

    def __str__(self):
        return self.description + str(self.subject) + str(self.uploaded_by)

class UserAnswer(models.Model):
    answer_sheet = models.ForeignKey(UserAnswerSheet, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.PROTECT)
    answer_text = models.TextField()
    marks = models.IntegerField()
    scored_marks = models.IntegerField(default=0)

    def __str__(self):
        return str(self.question) + str(self.answer_sheet)
