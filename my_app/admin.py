from django.contrib import admin
from my_app import models
# Register your models here.

admin.site.site_header = 'NITD Results'

admin.site.register(models.Student)