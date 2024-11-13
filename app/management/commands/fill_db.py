from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from app.models import Question, Answer, Tag, QuestionLike, AnswerLike
import random
from faker import Faker

fake = Faker()

class Command(BaseCommand):
    help = 'Fill the database with test data'

    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int, help="Multiplier for test data size")

    def handle(self, *args, **options):
        ratio = options['ratio']

        # Создание уникальных пользователей
        users = []
        for _ in range(ratio):
            username = fake.unique.user_name()  # использование fake.unique для уникальных имен пользователей
            user = User.objects.create_user(username=username, password='password')
            users.append(user)

        # Создание уникальных тегов
        tags = []
        for _ in range(ratio):
            tag_name = fake.unique.word()  # использование fake.unique для уникальных имен тегов
            tag = Tag.objects.create(name=tag_name)
            tags.append(tag)
        
        # Создание вопросов
        questions = []
        for _ in range(ratio * 10):
            question = Question.objects.create(
                author=random.choice(users),
                title=fake.sentence(),
                text=fake.sentence(),
            )
            question.tags.add(*random.sample(tags, 3))  # случайно добавляем 3 тега
            questions.append(question)
        
        # Создание ответов
        answers = []
        for _ in range(ratio * 100):
            answer = Answer.objects.create(
                question=random.choice(questions),
                author=random.choice(users),
                text=fake.text(),
            )
            answers.append(answer)

        # Создание уникальных лайков на вопросы
        question_likes = set()  # Множество для уникальных лайков
        for _ in range(ratio * 200):
            user = random.choice(users)
            question = random.choice(questions)
            if (user, question) not in question_likes:  # Проверка на уникальность пары (пользователь, вопрос)
                QuestionLike.objects.create(user=user, question=question)
                question_likes.add((user, question))
        
        # Создание уникальных лайков на ответы
        answer_likes = set()  # Множество для уникальных лайков
        for _ in range(ratio * 200):
            user = random.choice(users)
            answer = random.choice(answers)
            if (user, answer) not in answer_likes:  # Проверка на уникальность пары (пользователь, ответ)
                AnswerLike.objects.create(user=user, answer=answer)
                answer_likes.add((user, answer))

        self.stdout.write(self.style.SUCCESS(f'Successfully filled the database with {ratio} users, {ratio*10} questions, {ratio*100} answers, {ratio} tags, and {ratio*200} likes.'))
