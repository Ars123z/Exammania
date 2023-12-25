from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    
    phone_no = models.CharField(max_length=15, blank=True, null=True)
    
    STANDARD_CHOICES = (
        ('9th', '9th Grade'),
        ('10th', '10th Grade'),
        ('11th', '11th Grade'),
        ('12th', '12th Grade'),
        ('12th+', '12th Grade and Above'),
    )
    standard = models.CharField(max_length=10, choices=STANDARD_CHOICES, blank=True, null=True)
    
    # Fields for subscription
    is_subscriber = models.BooleanField(default=False)
    subscription_type = models.CharField(
        max_length=10, 
        choices=[('monthly', 'Monthly'), ('yearly', 'Yearly')],
        blank=True, null=True
    )
    subscription_start_date = models.DateTimeField(null=True, blank=True)
    subscription_end_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.user.username
    
    
class SubcriptionInfo(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    activation_date= models.DateTimeField(null=True, blank=True)
    expiry_date= models.DateTimeField(null=True, blank=True)
    amount= models.IntegerField()
    order_id= models.CharField(max_length=200)
    payment_id= models.CharField(max_length=200)
    paid= models.BooleanField(default=False)
    subscription_type = models.CharField(
    max_length=10, 
    choices=[('monthly', 'Monthly'), ('yearly', 'Yearly')],
    blank=True, null=True
)
    def __str__(self):
        return self.order_id
    




