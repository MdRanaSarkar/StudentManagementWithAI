from django.db import models
from student.models import Courses,Students
# Create your models here.
import random
from django.contrib.auth.models import User
# Create your models here.

DIFF_CHOICES = (
    ('easy', 'easy'),
    ('medium', 'medium'),
    ('hard', 'hard'),
)

class Quiz(models.Model):
    name = models.CharField(max_length=120)
    topic = models.CharField(max_length=120)
    number_of_questions = models.IntegerField()
    time = models.IntegerField(help_text="duration of quiz in minutes")
    required_score_to_pass = models.IntegerField(help_text=" required score in %")
    difficulty = models.CharField(max_length=6, choices=DIFF_CHOICES)
    course = models.ForeignKey(Courses, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}-{self.topic}"

    def get_questions(self):
        questions = list(self.question_set.all())
        random.shuffle(questions,)
        return questions[:self.number_of_questions]

    class Meta:
        verbose_name_plural = 'Quizzes'

class Question(models.Model):
    text = models.CharField(max_length=200)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.text)

    def get_answer(self):
        return self.answer_set.all()

class Answer(models.Model):
    text = models.CharField(max_length=200)
    correct = models.BooleanField(default=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"question:{self.question.text}, answer:{self.text}, correct:{self.correct}"

class FinalResult(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    student = models.ForeignKey(Students, on_delete=models.CASCADE)
    score = models.FloatField()

    def __str__(self):
        return f"{self.student.admin.username}, Score: {self.score}"