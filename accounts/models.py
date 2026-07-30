from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    STATE_CHOICES = [
        ('AP', 'Andhra Pradesh'), ('AR', 'Arunachal Pradesh'), ('AS', 'Assam'),
        ('BR', 'Bihar'), ('CG', 'Chhattisgarh'), ('GA', 'Goa'), ('GJ', 'Gujarat'),
        ('HR', 'Haryana'), ('HP', 'Himachal Pradesh'), ('JH', 'Jharkhand'),
        ('KA', 'Karnataka'), ('KL', 'Kerala'), ('MP', 'Madhya Pradesh'),
        ('MH', 'Maharashtra'), ('MN', 'Manipur'), ('ML', 'Meghalaya'),
        ('MZ', 'Mizoram'), ('NL', 'Nagaland'), ('OD', 'Odisha'), ('PB', 'Punjab'),
        ('RJ', 'Rajasthan'), ('SK', 'Sikkim'), ('TN', 'Tamil Nadu'),
        ('TS', 'Telangana'), ('TR', 'Tripura'), ('UP', 'Uttar Pradesh'),
        ('UK', 'Uttarakhand'), ('WB', 'West Bengal'), ('DL', 'Delhi'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=15)
    state = models.CharField(max_length=2, choices=STATE_CHOICES)
    tender_interests = models.CharField(max_length=500)

    def __str__(self):
        return f"{self.user.username}'s Profile"
