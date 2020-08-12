from django.db import models
from .employee import Employee
from .training_program import TrainingProgram

class EmployeeTrainingProgram(models.Model):

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    training_program = models.ForeignKey(TrainingProgram, on_delete=models.CASCADE)

    class Meta:
        verbose_name = ("Training Program")
        verbose_name_plural = ("Training Programs")