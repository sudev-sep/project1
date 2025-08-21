from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class User(AbstractUser):
    usertype=models.CharField(max_length=50)
    address=models.CharField(max_length=255,null=True)
    phone_number=models.IntegerField(null=True)

class Teacher(models.Model):
    teacher_id=models.ForeignKey(User, on_delete=models.CASCADE)
    salary=models.IntegerField()
    experience=models.IntegerField()

class Student(models.Model):
    student_id=models.ForeignKey(User, on_delete=models.CASCADE)
    guardian=models.CharField(max_length=30)
