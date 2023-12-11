from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.db import transaction
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm, AuthForm, QuestionForm
from .models import Test, Question, Answer, UserTest, UserAnswer


def index(request):
    tests = Test.objects.order_by('-id')
    return render(request, 'main/index.html', {'tests': tests})


def registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('idx')
    form = RegistrationForm()
    return render(request, 'main/registration_template.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('idx')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    form = AuthForm()
    return render(request, 'main/login_template.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('idx')


def test_view(request, test_id):
    return render(request, 'main/test_template.html', {'test': get_object_or_404(Test, id=test_id)})


@login_required
def question_view(request, test_id, question_order):
    all_questions = Question.objects.filter(test=test_id).order_by('order')
    if all_questions.last().order < question_order:
        return redirect('summary', test_id)
    question_obj = get_object_or_404(Question, test=test_id, order=question_order)
    test_obj = get_object_or_404(Test, id=test_id)
    if request.method == 'POST':
        form = QuestionForm(request.POST, question_obj.id)
        if form.is_valid():
            request.session[question_obj.id] = form.cleaned_data.get('question').id
            return redirect('/test/%s/%s' % (test_id, question_order+1))
    form = QuestionForm(question_id=question_obj.id)
    return render(request, 'main/question_template.html', {'question': question_obj, 'test':test_obj, 'form':form})


@login_required
def summary(request, test_id):
    all_questions = Question.objects.filter(test=test_id)
    if 'Finish' in request.POST:
        with transaction.atomic():
            test = UserTest.objects.create(user=request.user, test=get_object_or_404(Test, id=test_id))
            for el in all_questions:
                test = get_object_or_404(UserTest, id=test.id)
                question = get_object_or_404(Question, id=el.id)
                answer = get_object_or_404(Answer, id=request.session[str(el.id)])
                UserAnswer.objects.create(user_test=test, question=question, answer=answer)
                if answer.correct:
                    if test.score:
                        test.score += question.weight
                    else:
                        test.score = question.weight
                test.save()
                del request.session[str(el.id)]
        return redirect('idx')
    result = {}
    session = request.session
    for el in all_questions:
        result[el.id] = get_object_or_404(Answer, id=request.session[str(el.id)]).description
    return render(request, 'main/summary.html', {'result': result})


@login_required
def profile(request):
    tests = UserTest.objects.filter(user=request.user)
    data = {}
    for test in tests:
        data[test] = UserAnswer.objects.filter(user_test=test)
    return render(request, 'main/profile.html', {'data': data})
