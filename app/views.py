from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def paginate(objects_list, request, per_page=10):
    paginator = Paginator(objects_list, per_page)
    page = request.GET.get('page')
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    return page_obj

def get_popular_tags():
    return [
        {'name': 'python'},
        {'name': 'django'},
        {'name': 'javascript'},
        {'name': 'html'},
        {'name': 'css'},
        {'name': 'bootstrap'},
        {'name': 'jquery'},
        {'name': 'react'},
        {'name': 'vue'},
        {'name': 'angular'},
    ]

def get_best_members():
    return [
        {'username': 'Mr.Freeman'},
        {'username': 'Dr.House'},
        {'username': 'Bender'},
        {'username': 'Queen Victoria'},
        {'username': 'V.Pupkin'},
    ]

# Главная страница - список новых вопросов
def index(request):
    questions = []
    for i in range(1, 30):
        questions.append({
            'title': 'Title ' + str(i),
            'id': i,
            'text': 'text' + str(i)
        })
    popular_tags = get_popular_tags()
    best_members = get_best_members()

    questions = paginate(questions, request)
    context = {
        'questions': questions,
        'popular_tags': popular_tags,
        'best_members': best_members,
    }
    return render(request, 'index.html', context)

# Список "лучших" вопросов
def hot(request):
    questions = []
    for i in range(1, 30):
        questions.append({
            'title': 'Title ' + str(i),
            'id': i,
            'text': 'text' + str(i)
        })
    popular_tags = get_popular_tags()
    best_members = get_best_members()

    questions = paginate(questions, request)
    context = {
        'questions': questions,
        'popular_tags': popular_tags,
        'best_members': best_members,
    }
    return render(request, 'hot.html', context)

# Вопросы по тегу
def tag(request, tag_name):
    questions = []
    for i in range(1, 10):
        questions.append({
            'title': f'Tagged {tag_name} Question ' + str(i),
            'id': i,
            'text': f'Text of question tagged {tag_name} ' + str(i)
        })
    questions = paginate(questions, request)
    context = {
        'questions': questions,
        'tag_name': tag_name,
    }
    return render(request, 'tag.html', context)

# Страница одного вопроса со списком ответов
def question(request, question_id):
    questions = []
    for i in range(1, 30):
        questions.append({
            'title': 'Title ' + str(i),
            'id': i,
            'text': 'text' + str(i)
        })
    question = next((q for q in questions if q['id'] == question_id), None)
    
    if not question:
        return render(request, '404.html', status=404)

    popular_tags = get_popular_tags()
    best_members = get_best_members()

    context = {
        'question': question,
        'popular_tags': popular_tags,
        'best_members': best_members,
    }
    return render(request, 'question.html', context)

# Форма логина
def login_view(request):
    popular_tags = get_popular_tags()
    best_members = get_best_members()

    context = {
        'popular_tags': popular_tags,
        'best_members': best_members,
    }
    return render(request, 'login.html', context)

# Форма регистрации
def signup(request):
    popular_tags = get_popular_tags()
    best_members = get_best_members()

    context = {
        'popular_tags': popular_tags,
        'best_members': best_members,
    }
    return render(request, 'signup.html', context)

# Форма создания вопроса
def ask(request):
    popular_tags = get_popular_tags()
    best_members = get_best_members()

    context = {
        'popular_tags': popular_tags,
        'best_members': best_members,
    }
    return render(request, 'ask.html', context)

# Настройки пользователя
def settings(request):
    # Вы можете передать сюда данные для текущего пользователя
    user = request.user
    context = {
        'username': user.username,
        'email': user.email,
        # 'avatar': user.avatar или другие данные
    }
    return render(request, 'settings.html', context)