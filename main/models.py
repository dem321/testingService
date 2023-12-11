from django.db import models
from django.contrib.auth.models import User


class Test(models.Model):
    description = models.CharField('Описание теста', max_length=300)
    name = models.CharField('Название теста', max_length=30)

    def __str__(self):
        return str(self.name)


class Question(models.Model):
    description = models.CharField('Текст вопроса', max_length=200)
    order = models.PositiveIntegerField('Очередь вопроса')
    weight = models.PositiveIntegerField('Вес вопроса')
    test = models.ForeignKey(Test, verbose_name='Тест', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.description)


class Answer(models.Model):
    description = models.CharField('Текст ответа', max_length=100)
    correct = models.BooleanField('Правильность ответа')
    question = models.ForeignKey(Question, verbose_name='Вопрос', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.description)


class UserTest(models.Model):
    score = models.PositiveIntegerField('Оценка', null=True, blank=True)
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    test = models.ForeignKey(Test, verbose_name='Тест', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user) + '>>' + str(self.test)


class UserAnswer(models.Model):
    user_test = models.ForeignKey(UserTest, verbose_name='Пользователь', on_delete=models.CASCADE)
    question = models.ForeignKey(Question, verbose_name='Вопрос', on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, verbose_name='Ответ', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user_test) + '>>' + str(self.question) + '>>' + str(self.answer)
