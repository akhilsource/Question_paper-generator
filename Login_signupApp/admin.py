from django.contrib import admin


from .models import Register,UserProfile
# Register your models here.
admin.site.register(Register)
admin.site.register(UserProfile)