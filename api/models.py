from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models

class TimeStampedModel(models.Model): #TODO - move to utils model
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

ROLES = (
    ('tutor', 'Tutor'),
    ('tutee', 'Tutee'),
)

class User(AbstractUser):
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True, max_length=254)
    birth_date = models.DateField(auto_now=False, auto_now_add=False, null=True)
    image = models.ImageField(upload_to=None, height_field=None, width_field=None, max_length=None)
    role = models.CharField(max_length=10, choices=ROLES)
    is_verified = models.BooleanField(default=False)
    
    reset_pw_code = models.CharField(default=None, blank=True, null=True, max_length=12)
    reset_pw_exp = models.DateTimeField(default=None, blank=True, null=True) #add 5 mins to current time
    
    objects = UserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return '%s %s' % (self.first_name, self.last_name)

class Tutor(TimeStampedModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='tutor')
    rating = models.IntegerField(default=0)
    about_me = models.TextField(blank=True)

    def __str__(self):
        return self.user.email

class Tutee(TimeStampedModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='tutee')

    def __str__(self):
        return 'uid:%s | %s' % (self.user.id, self.user.email)
    

class Schedule(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_schedules')
    subject = models.CharField(null=True, blank=True, max_length=50)
    datetime_start = models.DateTimeField()
    datetime_end = models.DateTimeField()
    is_available = models.BooleanField(default=True)
    #is_archived = models.BooleanField(default=False)
    
    def __str__(self):
        return '%s @ %s to %s -- %s' % (self.datetime_start.date(), self.datetime_start.time(), self.datetime_end.time(), self.user.email)
    
    @property
    def duration_in_mins(self):
        min = (self.datetime_end - self.datetime_start) / 60
        return int(min.total_seconds())
    
class Appointment(TimeStampedModel):
    
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('declined', 'Declined'),
        ('approved', 'Approved'),
        ('canceled', 'Canceled')
    )
    
    tutee = models.ForeignKey(Tutee, on_delete=models.CASCADE, related_name='appointment_tutee')
    tutor_schedule = models.OneToOneField(Schedule, on_delete=models.PROTECT, related_name='appointment_tutor_schedule')
    status = models.CharField(default='pending', choices=STATUS_CHOICES, max_length=20)
    description = models.TextField(null=True, blank=True)
    reason_for_cancel = models.CharField(null=True, blank=True, max_length=150)
    is_archived = models.BooleanField(default=False)
    
    def __str__(self):
        return 'TUTEE: %s and TUTOR: %s [SCHED ID: %s]' % (self.tutee.user.email, self.tutor_schedule.user.email, self.tutor_schedule.id)