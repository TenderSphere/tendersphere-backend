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


class Tender(models.Model):
    CATEGORY_CHOICES = [
        ('Construction', 'Construction'),
        ('IT & Software', 'IT & Software'),
        ('Healthcare', 'Healthcare'),
        ('Defence', 'Defence'),
        ('Education', 'Education'),
        ('Transport', 'Transport'),
        ('Energy', 'Energy'),
        ('Agriculture', 'Agriculture'),
        ('Insurance & Financial Services', 'Insurance & Financial Services'),
        ('Consultancy & Professional Services', 'Consultancy & Professional Services'),
        ('Manufacturing & Supply', 'Manufacturing & Supply'),
        ('Facility Management', 'Facility Management'),
        ('Telecommunications', 'Telecommunications'),
        ('Water & Sanitation', 'Water & Sanitation'),
        ('Legal & Compliance', 'Legal & Compliance'),
        ('Miscellaneous', 'Miscellaneous'),
    ]

    title = models.CharField(max_length=300)
    description = models.TextField()
    department = models.CharField(max_length=200)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    state = models.CharField(max_length=2, choices=UserProfile.STATE_CHOICES)
    tender_value = models.CharField(max_length=100, blank=True)
    deadline = models.DateField()
    reference_number = models.CharField(max_length=100, unique=True)
    document_link = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    document_link = models.URLField(blank=True)
    portal_tender_id = models.CharField(max_length=100, blank=True, help_text="Admin-only: original portal's Tender ID for re-searching later")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
