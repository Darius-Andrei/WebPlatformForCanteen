from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import *

admin.site.register(newUser)
admin.site.register(newProduct)
admin.site.register(cos)
admin.site.register(orderedItem)
admin.site.register(newChef)
admin.site.register(newContact)
UserAdmin.list_display = ('username', 'is_staff', 'last_login', 'is_active')
UserAdmin.list_display_links = ('username',)
UserAdmin.list_editable = ('is_active',)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
