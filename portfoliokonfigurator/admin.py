from django.contrib import admin
from .models import GlobalSettings, Qualitaetsfaktor, QualitaetsfaktorKategorie

admin.site.register(GlobalSettings)
admin.site.register(QualitaetsfaktorKategorie)


@admin.register(Qualitaetsfaktor)
class QualitaetsfaktorAdmin(admin.ModelAdmin):
    list_display = ('name', 'currency_value', 'last_updated')
    search_fields = ('name', 'description')
