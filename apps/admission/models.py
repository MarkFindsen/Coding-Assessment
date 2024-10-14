from django.db import models


class Course(models.Model):
    name = models.CharField(max_length=50, blank=False)

    def __str__(self):
        return f"{self.name}"

class Intake(models.Model):
    pass
