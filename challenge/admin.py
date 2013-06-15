from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
import challenge.models as db


class UserInline(admin.StackedInline):
    model = db.Challenge_User
    can_delete = False
    verbose_name_plural = 'Challenge User'


class UserAdmin(UserAdmin):
    inlines = (UserInline, )


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(db.Challenge)
admin.site.register(db.Vote)
admin.site.register(db.Award)
admin.site.register(db.Claim)
admin.site.register(db.Category)
