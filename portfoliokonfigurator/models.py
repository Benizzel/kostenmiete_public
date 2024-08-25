from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from simple_history.models import HistoricalRecords


# TODO: Max one occurrence of the parameter on the UI and on Admin!
# Funktioniert theoretisch schon, weil wenn "neu" macht die App einfach ein Update (def save) - geht vielleicht noch
# schöner mit einem Singleton ansatz
class GlobalSettings(models.Model):
    referenzzinssatz = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Referenzzinssatz in Prozent"
    )
    kapitalisierungsfaktor = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Kapitalisierungsfaktor in Prozent"
    )
    history = HistoricalRecords()

    class Meta:
        verbose_name = "Globale Einstellungen"
        verbose_name_plural = "Globale Einstellungen"

    def __str__(self):
        return "Globale Einstellungen"

    def save(self, *args, **kwargs):
        if not self.pk and GlobalSettings.objects.exists():
            # If you're trying to create a new object and one already exists,
            # just update the existing one.
            return GlobalSettings.objects.first().save()
        return super(GlobalSettings, self).save(*args, **kwargs)

    @classmethod
    def load(cls):
        """
        easy way to get the current settings
        to get the settings use: "settings = GlobalSettings.load()"
        :return: Global Settings
        """
        obj, created = cls.objects.get_or_create(pk=1)
        return obj


class QualitaetsfaktorKategorie(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Qualitätsfaktor-Kategorie"
        verbose_name_plural = "Qualitätsfaktor-Kategorien"


def get_default_category():
    # The [0] at the end returns the QualitaetsfaktorKategorie instance
    # (rather than the tuple that get_or_create returns)
    return QualitaetsfaktorKategorie.objects.get_or_create(name="Sonstige")[0].id


class Qualitaetsfaktor(models.Model):
    kategorie = models.ForeignKey(
        QualitaetsfaktorKategorie,
        on_delete=models.PROTECT,
        related_name='qualitaetsfaktoren',
        default=get_default_category
    )
    name = models.CharField(max_length=100, blank=False, null=False)
    description = models.TextField(blank=False, null=False)
    currency_value = models.DecimalField(max_digits=6, decimal_places=2, blank=False, null=False)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.kategorie} - {self.name}: {self.currency_value}%"

    class Meta:
        verbose_name = "Qualitätsfaktor"
        verbose_name_plural = "Qualitätsfaktoren"
        unique_together = ['kategorie', 'name']
