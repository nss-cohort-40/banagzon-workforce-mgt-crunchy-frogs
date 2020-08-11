from django.db import models

class TrainingProgram(models.Model):

    title = models.CharField(max_length=55, default=None)
    description = models.CharField(max_length=200, default=None)
    start_date = models.DateField(default=None)
    end_date = models.DateField(default=None)
    capacity = models.IntegerField(default=None)

    class Meta:
        verbose_name = ("Training Program")
        verbose_name_plural = ("Training Programs")

    def __str__(self):
        return f"{self.title}"