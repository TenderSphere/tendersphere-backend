
from django.contrib import admin
from .models import UserProfile, Tender

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'state', 'tender_interests')

@admin.register(Tender)
class TenderAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'state', 'deadline', 'reference_number', 'portal_tender_id')
    list_filter = ('category', 'state')
    search_fields = ('title', 'department', 'reference_number', 'portal_tender_id')
