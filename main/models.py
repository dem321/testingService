from django.db import models
from django.contrib.auth.models import User


class Test(models.Model):
    description = models.CharField('Оаисание теста', max_length=300)
    name = models.CharField('Название теста', max_length=30)


class Question(models.Model):
    description = models.CharField('Текст вопроса', max_length=200)
    order = models.PositiveIntegerField('Очередь вопроса')
    weight = models.PositiveIntegerField('Вес вопроса')
    test = models.ForeignKey(Test, verbose_name='Тест', on_delete=models.CASCADE)


class Answer(models.Model):
    description = models.CharField('Текст ответа', max_length=100)
    correct = models.BooleanField('Правильность ответа')
    question = models.ForeignKey(Question, verbose_name='Вопрос', on_delete=models.CASCADE)


class UserTest(models.Model):
    score = models.PositiveIntegerField('Оценка')
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    test = models.ForeignKey(Test, verbose_name='Тест', on_delete=models.CASCADE)


class UserAnswer(models.Model):
    user_test = models.ForeignKey(UserTest, verbose_name='Пользователь', on_delete=models.CASCADE)
    question = models.ForeignKey(Question, verbose_name='Вопрос', on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, verbose_name='Ответ', on_delete=models.CASCADE)