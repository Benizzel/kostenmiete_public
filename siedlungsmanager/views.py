from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from .models import Siedlung, Objekt


class SiedlungHome(ListView):
    model = Siedlung
    template_name = 'siedlungsmanager/siedlung_home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['objekte'] = Objekt.objects.all()
        return context


class SiedlungCreate(CreateView):
    model = Siedlung
    template_name = 'siedlungsmanager/siedlung_create.html'
    fields = '__all__'
    # in contrast to reverse: reverse_lazy is waiting until db entry is done
    success_url = reverse_lazy('siedlung_home')


class SiedlungDetail(DetailView):
    model = Siedlung
    template_name = 'siedlungsmanager/siedlung_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get all Objekte associated with this Siedlung
        context['objekte'] = self.object.objekt_set.all()
        return context


class SiedlungUpdate(UpdateView):
    model = Siedlung
    template_name = 'siedlungsmanager/siedlung_update.html'
    fields = '__all__'


class SiedlungDelete(DeleteView):
    model = Siedlung
    template_name = 'siedlungsmanager/siedlung_delete.html'
    success_url = reverse_lazy('siedlung_home')


class ObjektCreate(CreateView):
    model = Objekt
    template_name = 'siedlungsmanager/objekt_create.html'
    fields = ['internal_oid']

    def form_valid(self, form):
        siedlung_pk = self.kwargs.get('pk')
        siedlung = get_object_or_404(Siedlung, pk=siedlung_pk)
        form.instance.siedlung = siedlung
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('siedlung_detail', kwargs={'pk': self.object.siedlung.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        siedlung_pk = self.kwargs.get('pk')
        context['siedlung'] = get_object_or_404(Siedlung, pk=siedlung_pk)
        return context

