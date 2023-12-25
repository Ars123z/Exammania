from django.contrib import admin
from .models import UserProfile, SubcriptionInfo

# Register your models here.
class SubcriptionInfoAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'payment_id', 'paid', 'subscription_type', 'activation_date', 'expiry_date', 'amount')
    search_fields= ['order_id', 'payment_id', 'user__username']


admin.site.register(UserProfile)
admin.site.register(SubcriptionInfo, SubcriptionInfoAdmin)