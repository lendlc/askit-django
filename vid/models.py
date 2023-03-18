from django.db import models
from api.models import TimeStampedModel, Tutor

class Video(TimeStampedModel):
    title = models.CharField(max_length=255)
    description = models.TextField()
    file = models.FileField(upload_to='videos/')
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.id} | {self.tutor.user.email} - {self.title}'
    