from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('login', views.loginUser, name="login"),
    path('logout', views.logoutUser, name="logout"),
    path('signup', views.signupUser, name="signup"),
    path('home', views.home, name="home"),
    path('upload_question', views.uploadQuestion, name="upload_question"),
    path('upload_book', views.uploadBook, name="upload_book"),
    path('get_solution', views.getSolution, name="get_solution"),
    path('correct_answer_sheet', views.correctAnswerSheet, name="correct_answer_sheet"),
]
