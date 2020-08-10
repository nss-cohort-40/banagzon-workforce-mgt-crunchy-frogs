from django.db import models

class TrainingProgram(models.Model):

    title = models.CharField(max_length=55)
    start_date = models.DateField()
    end_date = models.DateField()
    capacity = models.IntegerField()

    class Meta:
        verbose_name = ("Training Program")
        verbose_name_plural = ("Training Programs")

    def __str__(self):
        return f"{self.title}"