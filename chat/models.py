from django.db import models
from api.models import TimeStampedModel, Appointment, Tutee, Tutor, User

# Create your models here.
class Conversation(TimeStampedModel):
    tutor = models.ForeignKey(Tutor, related_name='convo_tutor', on_delete=models.CASCADE)
    tutee = models.ForeignKey(Tutee, related_name='convo_tutee', on_delete=models.CASCADE)
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return f'{self.id} | {self.tutor.user.email} and {self.tutee.user.email}'
    
    
class Message(TimeStampedModel):
    conversation = models.ForeignKey(Conversation, related_name='messages', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='message_sender', on_delete=models.CASCADE)
    message = models.TextField()
    
    def __str__(self):
        return f'[{self.conversation.id}] {self.user.email} said {self.message}'
    
    
    