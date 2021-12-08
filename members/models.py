from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserRoles(models.Model):

    ROLE_CHOICES = (
        ('Student', 'Student'),
        ('Verifier', 'Verifier'),
        ('Payer', 'Payer'),
        ('Graduate', 'Graduate'),
        ('Admin', 'Admin'),
    )

    name = models.CharField('name', choices=ROLE_CHOICES, max_length=100)

    def __str__(self):
        return str(self.name)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) #if user is deleted the profile will be deleted as well,but if profile is deleted , user won’t be deleted
    phone = models.CharField(max_length=100, null=True, blank=True)
    title = models.ForeignKey(UserRoles, null=True, on_delete=models.SET_NULL) #Student, Verifier, FinancialGuy
    salary = models.FloatField(default=0)
    inboxNotification = models.BooleanField(default=False)

    def __str__(self):
        return str(self.title)