from django.db import models

# Create your models here.

class Event(models.Model):
    title = models.CharField(max_length=50)
    location = models.CharField(max_length=50)
    date = models.CharField(max_length=50)
    description = models.TextField()

    
    def __str__(self):
        return self.title


class Applicant(models.Model):
    full_name = models.CharField(max_length=50)    
    email = models.EmailField()
    phone = models.CharField(max_length=10)
    event = models.ForeignKey('Event', on_delete=models.CASCADE)

   
    def __str__(self):
        return self.full_name

