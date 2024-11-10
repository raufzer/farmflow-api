from django.db import models

# Create your models here.
class Expert(models.Model):
    expert_job = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    studies_degree = models.CharField(max_length=255)
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=0)
    contact_number = models.CharField(max_length=255)
    
    def __str__(self):
        return self.expert_job