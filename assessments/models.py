from django.db import models
from academics.models import Course
from accounts.base_models import TimeStampedModel
from academics.models import Course

class Assessment(TimeStampedModel):
    title = models.CharField(max_length=255)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    total_marks = models.PositiveIntegerField()

    def __str__(self):
        return self.title

class Question(models.Model):
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE)
    text = models.TextField()
    marks = models.IntegerField()
