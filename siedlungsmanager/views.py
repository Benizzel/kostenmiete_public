from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from .models import Siedlung


class SiedlungHome(ListView):
    model = Siedlung
    template_name = 'siedlungsmanager/siedlung_home.html'


class SiedlungCreate(CreateView):
    model = Siedlung
    template_name = 'siedlungsmanager/siedlung_create.html'
    fields = '__all__'
    # in contrast to reverse: reverse_lazy is waiting until db entry is done
    success_url = reverse_lazy('siedlung_home')


class SiedlungDetail(DetailView):
    model = Siedlung
    template_name = 'siedlungsmanager/siedlung_detail.html'


class SiedlungUpdate(UpdateView):
    model = Siedlung
    template_name = 'siedlungsmanager/siedlung_update.html'
    fields = '__all__'

class SiedlungDelete(DeleteView):
    model = Siedlung
    template_name = 'siedlungsmanager/siedlung_delete.html'
    success_url = reverse_lazy('siedlung_home')

