from django.db import models
from django.contrib.auth.models import User


class Discount(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    percent = models.FloatField(blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=15, default='waiting')
    staff_decisions = models.CharField(
        max_length=100, blank=True, null=True)

    def __str__(self):
        return f'{self.id} - {self.user.username}'


class POS(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    serial_number = models.CharField(
        max_length=15, blank=True, null=True)

    def __str__(self):
        return f'{self.serial_number} - {self.user.username}'
