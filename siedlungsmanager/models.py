from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.urls import reverse


class Objekt(models.Model):
    internal_oid = models.CharField(
        verbose_name='OID',
        unique=True,
        max_length=10,
        help_text="Maximal 10 Zeichen"
    )
    siedlung = models.ForeignKey(
        'Siedlung',
        on_delete=models.CASCADE
    )

    class Meta:
        ordering = ['internal_oid']


class Siedlung(models.Model):
    internal_id = models.CharField(
        verbose_name='Interne ID',
        unique=True,
        max_length=5,
        help_text='Maximal 5 Zeichen'
    )
    bezeichnung = models.CharField(
        verbose_name='Bezeichnung',
        max_length=120,
        help_text='Maximal 120 Zeichen'
    )
    anlagewert = models.IntegerField(
        verbose_name='Anlagewert',
        help_text='Auch bekannt als Anlagekosten oder Investitionswert. Erfassen ohne Nachkommastellen.'
    )
    versicherungswert = models.IntegerField(
        verbose_name='GVZ-Wert',
        help_text='Versicherungswert gem. GVZ Police. Erfassen ohne Nachkommastellen.'
    )
    baurechtszins = models.IntegerField(
        verbose_name='Baurechtszins',
        blank=True,
        null=True,
    )
    betriebsquote_zuschlag = models.DecimalField(
        verbose_name='Betriebsquote Zuschlag',
        max_digits=5,
        decimal_places=2,
        validators=[
            MinValueValidator(0.00),
            MaxValueValidator(100.00)
        ],
        blank=True,
        null=True,
        help_text='Erfasse einen Wert zwischen 0 und 100 mit maximal zwei Nachkommastellen'
    )

    class Meta:
        ordering = ['internal_id']

    def __str__(self):
        return f"{self.internal_id} {self.bezeichnung}"

    def get_absolute_url(self):
        return reverse('siedlung_detail', args=[str(self.id)])
