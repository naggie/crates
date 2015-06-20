from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from models import Profile
from django.contrib.auth.models import Group

# Groups are not used, in favor of per-user flags.
# Crates use case involves just a handful of users.
admin.site.unregister(Group)
# We're extending this to include profile elements
admin.site.unregister(User)



class ProfileInlineAdmin(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'API Access'
    readonly_fields = ('bytes_inbound','bytes_outbound','object_count','bytes_available','bytes_total','objects_common')

@admin.register(User)
class CratesUserAdmin(UserAdmin):
    inlines = (ProfileInlineAdmin, )

    list_display = ('__unicode__','is_superuser')#,'profile_has_api_access','can_upload')
    search_fields = list_display

    # override this to remove useless (to crates) group/permissions
    fieldsets = (
        ('Credentials',         {'fields': ('username', 'password')}),
        ('Personal info',       {'fields': ('first_name', 'last_name', 'email')}),
        ('General Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser',)}),
        ('Important dates',     {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username','first_name','last_name','email','password1', 'password2','is_superuser'),
        }),
    )
