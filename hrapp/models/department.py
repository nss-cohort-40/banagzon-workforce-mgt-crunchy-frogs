from django.db import models

class Department(models.Model):

    dept_name = models.CharField(max_length=25)
    budget = models.DecimalField(max_digits=20, decimal_places=2)

    class Meta:
        verbose_name = ("Department")
        verbose_name_plural = ("Departments")

    def __str__(self):
        return f"{self.dept_name}"