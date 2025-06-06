from django.db import models
from django.contrib.auth.models import User


class Tag(models.Model):
    name = models.CharField(max_length=30)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Task(models.Model):
    PRIORITY_CHOICES = [
        ('1', 'Alta'),
        ('2', 'Média'),
        ('3', 'Baixa'),
    ]


    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    completed = models.BooleanField(default=False)
    due_date = models.DateField(null=True, blank=True)
    priority = models.CharField(max_length=1, choices=PRIORITY_CHOICES, default='2')
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return self.title