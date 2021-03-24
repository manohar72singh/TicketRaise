from django.contrib import admin
from . models import *
# Register your models here.

admin.site.register(UserType)
admin.site.register(User)
admin.site.register(Logindetail)
admin.site.register(Ticket)
admin.site.register(Category)
admin.site.register(Ticket_type)