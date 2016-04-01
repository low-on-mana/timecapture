from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import TimeUser,DEFAULT_USER_PASSWORD

class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields"""
    class Meta:
        model = TimeUser
        fields = ('email','is_staff')

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(DEFAULT_USER_PASSWORD)
        if commit:
            user.save()
        return user

class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    class Meta:
        model = TimeUser
        fields = ('email','is_active', 'is_staff','cost_per_hr')


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('email','first_name','last_name', 'is_staff','is_active')
    list_filter = ('is_staff',)
    fieldsets = (
        (None, {'fields': ('email',)}),
        # ('Personal info', {'fields': ('date_of_birth',)}),
        ('Professional info', {'fields': ('cost_per_hr',)}),
        ('Permissions', {'fields': ('is_staff','is_active')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email','is_staff')} 
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()

admin.site.register(TimeUser, UserAdmin)
admin.site.unregister(Group)
admin.site.site_header = 'Tenet Administration'
admin.site.site_title = 'Welcome Tenet Admin'
