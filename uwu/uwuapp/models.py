from django.db import models

# Create your models here.
class Manga(models.Model):
    name = models.CharField(max_length=128)
    author = models.CharField(max_length=128)
    date = models.DateField()
    is_finished = models.BooleanField()

    def __str__(self):
        return self.name