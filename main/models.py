from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class ToDo(models.Model):

    user = models.ForeignKey(User, related_name='userf', on_delete=models.CASCADE)
    
    label = models.CharField(max_length=150)

    description = models.TextField(null=True, blank=True)

    completed = models.BooleanField(default=False)

    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.label


