from django.db import models


class Message(models.Model):

    STATUS_CHOICES = [
        ('Ok', 'Ok'),
        ('Error', 'Error')
    ]

    sender = models.EmailField()
    body = models.TextField()
    status = models.CharField(max_length=5, choices=STATUS_CHOICES)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.sender
