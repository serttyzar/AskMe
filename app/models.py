from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count

class TagManager(models.Manager):
    def popular_tags(self):
        return self.annotate(num_questions=Count('questions')).order_by('-num_questions')[:10]

class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)
    objects = TagManager()

    def __str__(self):
        return self.name

class QuestionManager(models.Manager):
    def new_questions(self):
        return self.order_by('-created_at')

    def best_questions(self):
        return self.order_by('-likes')

class Question(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.TextField() 
    text = models.TextField()
    tags = models.ManyToManyField(Tag, related_name='questions')
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.PositiveIntegerField(default=0)

    objects = QuestionManager()

    def __str__(self):
        return self.text

    def get_absolute_url(self):
        return f"/questions/{self.id}/"

    def toggle_like(self, user):
        like, created = QuestionLike.objects.get_or_create(user=user, question=self)
        if not created:
            like.delete()
        return created

    class Meta:
        ordering = ['-created_at']

class Answer(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.text

    def toggle_like(self, user):
        like, created = AnswerLike.objects.get_or_create(user=user, answer=self)
        if not created:
            like.delete()
        return created

class ProfileManager(models.Manager):
    def best_members(self):
        return self.annotate(
            num_questions=Count('user__question'),
            num_answers=Count('user__answers')
        ).order_by('-num_questions', '-num_answers')[:10]

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

    objects = ProfileManager()

    def __str__(self):
        return self.user.username

class QuestionLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'question')

class AnswerLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'answer')