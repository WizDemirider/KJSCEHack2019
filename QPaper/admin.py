from django.contrib import admin
from .models import *

admin.site.register(Course)
admin.site.register(Subject)
admin.site.register(Question)
admin.site.register(QuestionPaper)
admin.site.register(UserAnswerSheet)
admin.site.register(UserAnswer)
admin.site.register(ReferenceBook)