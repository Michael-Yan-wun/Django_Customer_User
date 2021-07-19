from django.contrib import admin
from .models import NewUser
from django.contrib.auth.admin import UserAdmin
from django.forms import TextInput, Textarea

# config admin table(after superuser login)
class UserAdminConfig(UserAdmin):
    model = NewUser
    search_fields = ('email', 'user_name', 'first_name')
    list_filter = ('email', 'user_name', 'first_name', 'is_active', 'is_staff')
    ordering = ('-start_date',)
    list_display = ('email', 'user_name', 'first_name',
                    'is_active', 'is_staff')

    # which block to display
    fieldsets = (
        (None, {'fields': ('email', 'user_name', 'first_name')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
        ('Personal', {'fields': ('about',)})
    )

    # format setting
    formfield_overrides = {
        NewUser.about:{
            'widget':Textarea(attrs={
                'rows':10,
                'cols':40
            })
        },
    }
    # add new user fieldsets.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'user_name', 'first_name', 'password1','password2', 'is_active', 'is_staff')
        }),
    )


# Register models here.
admin.site.register(NewUser, UserAdminConfig)
