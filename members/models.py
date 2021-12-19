from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserRoles(models.Model):

    #choices of roles for Admin to add from Admin Panel. These will be the only options of roles
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

# Model of User Profile, each user should have one. It gives more attributes to each user than the default options.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) #if user is deleted the profile will be deleted as well,but if profile is deleted , user won’t be deleted
    phone = models.CharField(max_length=13, null=True, blank=True)
    title = models.ForeignKey(UserRoles, null=True, on_delete=models.SET_NULL) #Student, Verifier, FinancialGuy
    salary = models.FloatField(default=0)                       # remaining amount to be paid
    inboxNotification = models.BooleanField(default=False)      # notification when user has to read new message
    addedToTimesheet = models.BooleanField(default=False)       # notification to Verifier when a user adds a shift to his timesheet

    def __str__(self):
        return str(self.title)