from django.db import models
from django.core.exceptions import ValidationError
from django.utils.timezone import now

class Course(models.Model):
    name = models.CharField(max_length=50, blank=False)

    def __str__(self):
        return f"{self.name}"

class Intake(models.Model):
    start_date = models.DateField(blank=False)
    end_date = models.DateField(blank=False)
    course = models.ForeignKey(Course, blank=False, on_delete=models.CASCADE)

    def clean(self):
        super().clean()
        if self.start_date and self.end_date:
            if self.start_date > self.end_date:
                raise ValidationError({
                        'end_date': ('Intake end date cannot be before start date.'),
                    })

    def __str__(self):
        return f"{self.course.name}: {self.start_date} to {self.end_date}"
