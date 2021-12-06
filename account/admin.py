from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
# Register your models here.
from .models import *

class AccountAdmin(UserAdmin):
    list_display = ['email' , 'first_name','last_name','username','last_login','is_active','date_joined']
    list_display_links =  ['email' , 'first_name','last_name']
    readonly_fields =('date_joined','last_login')
    ordering =['date_joined',]

    filter_horizontal =()
    list_filter =()
    # this make the password read only
    fieldsets =()
       
admin.site.register(Account,AccountAdmin)