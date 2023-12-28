from django.contrib import admin
from django.contrib.auth.models import Group
from main.models import Account
# Register your models here.


@admin.action(description="Утвердить автора")
def make_author(modeladmin,request,queryset):
    group = Group.objects.get(name='Authors')
    ungroup = Group.objects.get(name='Actions Required')
    for user in queryset:
        user.groups.add(group)
        user.groups.remove(ungroup)


class AccountAdmin(admin.ModelAdmin):
    list_display = ['user','gender']
    list_filter = ['user','gender']
    #actions = [make_author]

from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

#@admin.register(User)
class CustomUserAdmin(UserAdmin):
     actions = [make_author]
#
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

admin.site.register(Account, AccountAdmin)





