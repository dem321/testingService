from django.contrib import admin

from .models import Test, UserTest, UserAnswer, Question, Answer
# Register your models here.
admin.site.register(Answer)
admin.site.register(Test)
admin.site.register(UserAnswer)
admin.site.register(UserTest)
admin.site.register(Question)
