from django.core.validators import MinValueValidator, MaxValueValidator
from .validators import validate_last_decimal_for_currency
from django.db import models
from django.urls import reverse


class Objekt(models.Model):
    BEREICH_2 = 'B2'
    BEREICH_3 = 'B3'
    BEREICH_4 = 'GZ'

    BEREICH_CHOICES = [
        (BEREICH_2, 'B2'),
        (BEREICH_3, 'B3'),
        (BEREICH_4, 'GZ')
    ]

    PUNKTE_1_5 = 5.5
    PUNKTE_2_0 = 6
    PUNKTE_2_5 = 6.5
    PUNKTE_3_0 = 7.5
    PUNKTE_3_5 = 8.0
    PUNKTE_4_0 = 9.0
    PUNKTE_4_5 = 9.5
    PUNKTE_5_0 = 10.5
    PUNKTE_5_5 = 11.5
    PUNKTE_6_0 = 12.5

    PUNKTE_CHOICES = [
        (PUNKTE_1_5, '5.5 Punkte - 1.5 Zimmer'),
        (PUNKTE_2_0, '6 Punkte - 2.0 Zimmer'),
        (PUNKTE_2_5, '6.5 Punkte - 2.5 Zimmer'),
        (PUNKTE_3_0, '7.5 Punkte - 3.0 Zimmer'),
        (PUNKTE_3_5, '8.0 Punkte - 3.5 Zimmer'),
        (PUNKTE_4_0, '9.0 Punkte - 4.0 Zimmer'),
        (PUNKTE_4_5, '10.0 Punkte - 4.5 Zimmer'),
        (PUNKTE_5_0, '10.5 Punkte - 5.0 Zimmer'),
        (PUNKTE_5_5, '11.5 Punkte - 5.5 Zimmer'),
        (PUNKTE_6_0, '12.0 Punkte - 6.0 Zimmer')
    ]

    internal_oid = models.CharField(
        verbose_name='OID',
        unique=True,
        max_length=10,
        help_text="Maximal 10 Zeichen"
    )
    bezeichnung = models.CharField(
        verbose_name='Bezeichnung',
        max_length=120,
        help_text='Maximal 120 Zeichen'
    )

    bereich = models.CharField(
        verbose_name='Bereich',
        max_length=2,
        choices=BEREICH_CHOICES,
        default=BEREICH_2
    )

    punkte = models.DecimalField(
        verbose_name='Punkte',
        choices=PUNKTE_CHOICES,
        decimal_places=1,
        max_digits=3,
        default=PUNKTE_3_5
    )

    aktuelle_miete = models.DecimalField(
        verbose_name='Aktuelle Miete',
        max_digits=10,
        decimal_places=2,
        default=0.00,
        validators=[MinValueValidator(0), validate_last_decimal_for_currency]
    )

    siedlung = models.ForeignKey(
        'Siedlung',
        on_delete=models.CASCADE,
        help_text='Achtung: ordnet das Objekt der ausgewählten Siedlung zu!'
    )

    class Meta:
        ordering = ['internal_oid']
        verbose_name = 'Objekt'
        verbose_name_plural = 'Objekte'

    def __str__(self):
        return f"{self.internal_oid} {self.bezeichnung}"

    def get_absolute_url(self):
        return reverse('objekt_detail', args=[str(self.id)])


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
    anlagewert = models.PositiveIntegerField(
        verbose_name='Anlagewert',
        help_text='Auch bekannt als Anlagekosten oder Investitionswert. Erfassen ohne Nachkommastellen.'
    )
    versicherungswert = models.PositiveIntegerField(
        verbose_name='GVZ-Wert',
        help_text='Versicherungswert gem. GVZ Police. Erfassen ohne Nachkommastellen.'
    )
    baurechtszins = models.PositiveIntegerField(
        verbose_name='Baurechtszins',
        blank=True,
        null=True,
        help_text='Baurechtszins falls vorhanden'
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
        help_text='Wert zwischen 0 und 100 mit maximal zwei Nachkommastellen'
    )

    class Meta:
        ordering = ['internal_id']
        verbose_name = 'Siedlung'
        verbose_name_plural = 'Siedlungen'

    def __str__(self):
        return f"{self.internal_id} {self.bezeichnung}"

    def get_absolute_url(self):
        return reverse('siedlung_detail', args=[str(self.id)])
