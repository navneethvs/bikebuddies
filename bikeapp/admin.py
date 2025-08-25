from django.contrib import admin
from . models import Reg_tbl,Pass_tbl,Bike_tbl,Feed_tbl
# Register your models here.
admin.site.register(Reg_tbl)
admin.site.register(Pass_tbl)
admin.site.register(Bike_tbl)
admin.site.register(Feed_tbl)