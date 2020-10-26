from django.contrib import admin
from tors_app.models import *

admin.site.register(tour)
admin.site.register(status)
admin.site.register(customer)
admin.site.register(reservation)
admin.site.site_header = "Welcome To TORS"
# Register your models here.
