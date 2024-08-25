from django.shortcuts import render
from django.views.generic import ListView

from .models import GlobalSettings, Qualitaetsfaktor


class Portfoliokonfiguration(ListView):
    # TODO: Create settings-view
    template_name = 'portfoliokonfiguration.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['globale_einstellungen'] = GlobalSettings.objects.all()
        context['qualitaetsfaktoren'] = Qualitaetsfaktor.objects.all()
        return context

