from django.db import models

class TestModel(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class SignalLog(models.Model):
    message = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message
