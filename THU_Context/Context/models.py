from django.db import models

# Create your models here.
class Task(models.Model):
    task_name = models.CharField(max_length=100)

class Key(models.Model):
    key_name = models.CharField(max_length=100)