from django.db import models

# Create your models here.
class Job(models.Model):
    job_name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=255)
    
    def __str__(self):
        return self.expert_job