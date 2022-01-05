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
