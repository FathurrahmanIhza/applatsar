from django.contrib import admin
from applatsar.models import *
# Register your models here.

class DBGempa(admin.ModelAdmin):
    list_display = ['stasiun','tanggal','jam','magnitudo','kedalaman', 'keterangan']
    search_fields = ['stasiun', 'keterangan']
    list_filter = ['stasiun']

class DBTamu(admin.ModelAdmin):
    list_display = ['nama','tanggal','instansi','agenda']

admin.site.register(Databasegempa, DBGempa)
admin.site.register(DatabaseTamu, DBTamu)
