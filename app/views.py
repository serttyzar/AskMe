from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from app.models import Profile, Tag, Question, Answer

# Пагинация
def paginate_queryset(request, queryset, per_page=10):
    paginator = Paginator(queryset, per_page)
    page = request.GET.get('page')
    return paginator.get_page(page)

def get_common_context():
    popular_tags = Tag.objects.popular_tags()
    best_members = Profile.objects.best_members()
    return {'popular_tags': popular_tags, 'best_members': best_members}


# Главная страница - список новых вопросов
def index(request):
    questions = paginate_queryset(request, Question.objects.new_questions())
    return render(request, 'index.html', {'questions': questions, **get_common_context()})

# Список "лучших" вопросов
def hot(request):
    questions = paginate_queryset(request, Question.objects.best_questions())
    return render(request, 'hot.html', {'questions': questions, **get_common_context()})

# Вопросы по тегу
def tag(request, tag_name):
    tag = get_object_or_404(Tag, name=tag_name)
    questions = paginate_queryset(request, tag.questions.all())
    return render(request, 'tag.html', {'questions': questions, 'tag_name': tag_name, **get_common_context()})

# Страница одного вопроса со списком ответов
def question(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    answers = paginate_queryset(request, question.answers.all())
    return render(request, 'question.html', {'question': question, 'answers': answers, **get_common_context()})

# Лайк на вопрос
@require_POST
@login_required
def like_question(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    question.toggle_like(request.user)
    return redirect('question', question_id=question_id)

# Лайк на ответ
@require_POST
@login_required
def like_answer(request, answer_id):
    answer = get_object_or_404(Answer, id=answer_id)
    answer.toggle_like(request.user)
    return redirect('question', question_id=answer.question.id)


# Форма логина
def login_view(request):
    context = get_common_context()
    return render(request, 'login.html', context)

# Форма регистрации
def signup(request):
    context = get_common_context()
    return render(request, 'signup.html', context)

# Форма создания вопроса
@login_required
def ask(request):
    context = get_common_context()
    return render(request, 'ask.html', context)

# Настройки пользователя
@login_required
def settings(request):
    context = {
        'username': request.user.username,
        'email': request.user.email,
        **get_common_context(),
    }
    return render(request, 'settings.html', context)    