from django.contrib import admin
from pos_app.models import User, TableUser, TableOrder

# Register your models here.
admin.site.register(User)
admin.site.register(TableUser)
admin.site.register(TableOrder)