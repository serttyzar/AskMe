from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),  # Главная страница
    path('hot/', views.hot, name='hot'),  # Горячие вопросы
    path('tag/<str:tag_name>/', views.tag, name='tag'),  # Вопросы по тегу
    path('question/<int:question_id>/', views.question, name='question'),  # Страница вопроса
    path('login/', views.login_view, name='login'),  # Форма логина
    path('signup/', views.signup, name='signup'),  # Форма регистрации
    path('ask/', views.ask, name='ask'),  # Форма создания вопроса
    path('settings/', views.settings, name='settings'),
]

