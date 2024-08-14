from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from .form import SiedlungForm, ObjektForm
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
    form_class = SiedlungForm
    # in contrast to reverse: reverse_lazy is waiting until db entry is done
    success_url = reverse_lazy('siedlung_home')


class SiedlungDetail(DetailView):
    model = Siedlung
    template_name = 'siedlungsmanager/siedlung_detail.html'

    def get_object(self, **kwargs):
        """
        Overrides the default get_object method.
        Returns the object the view is displaying.
        """
        # Extract the parameters from the URL
        siedlung_pk = self.kwargs.get('siedlung_pk')
        # Fetch the object using the parameters
        return get_object_or_404(Siedlung, pk=siedlung_pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get all Objekte associated with this Siedlung
        context['objekte'] = self.object.objekt_set.all()
        return context


class SiedlungUpdate(UpdateView):
    model = Siedlung
    template_name = 'siedlungsmanager/siedlung_update.html'
    # Defines that all field are included in the form which is passed to the html
    form_class = SiedlungForm

    def get_object(self, **kwargs):
        """
        Overrides the default get_object method.
        Returns the object the view is displaying.
        """
        # Extract the parameters from the URL
        siedlung_pk = self.kwargs.get('siedlung_pk')
        # Fetch the object using the parameters
        return get_object_or_404(Siedlung, pk=siedlung_pk)


class SiedlungDelete(DeleteView):
    model = Siedlung
    template_name = 'siedlungsmanager/siedlung_delete.html'
    success_url = reverse_lazy('siedlung_home')

    def get_object(self, **kwargs):
        """
        Overrides the default get_object method.
        Returns the object the view is displaying.
        """
        # Extract the parameters from the URL
        siedlung_pk = self.kwargs.get('siedlung_pk')
        # Fetch the object using the parameters
        return get_object_or_404(Siedlung, pk=siedlung_pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get all Objekte associated with this Siedlung
        context['objekte'] = self.object.objekt_set.all()
        return context


class ObjektCreate(CreateView):
    model = Objekt
    # Use Custom form to exclude attribute Siedlung from the UI
    form_class = ObjektForm
    template_name = 'siedlungsmanager/objekt_create.html'

    def get_form(self, form_class=None):
        """
        Excludes the siedlung-field from the form for the ObjektCreate View because
        siedlung is set to the siedlung of the context automatically within form_valid()
        """
        form = super().get_form(form_class)
        form.fields.pop('siedlung')
        return form

    def form_valid(self, form):
        """
        Overrides the default form validation.
        It sets the siedlung attribute of the new Objekt instance to Siedlung pk from the URL.
        This method is called when a valid form is submitted.
        """
        # It retrieves the Siedlung primary key from the URL.
        siedlung_pk = self.kwargs.get('siedlung_pk')
        # It gets the Siedlung object or returns a 404 error if not found.
        siedlung = get_object_or_404(Siedlung, pk=siedlung_pk)
        # It sets the siedlung attribute of the new Objekt instance.
        form.instance.siedlung = siedlung
        # It then calls the parent class's form_valid method to save the object.
        return super().form_valid(form)

    def get_success_url(self):
        """
        Overrides the default get_success_url
        This method determines where to redirect after successful form submission.
        It returns a URL to the detail view of the Siedlung associated with the newly created Objekt.
        """
        return reverse_lazy('siedlung_detail', kwargs={'siedlung_pk': self.object.siedlung.pk})

    def get_context_data(self, **kwargs):
        """
        Overrides the default get_context_data
        This method is used to add extra context data to the template.
        It retrieves the Siedlung object using the primary key from the URL.
        It adds this Siedlung object to the context, making it available in the template.
        """
        context = super().get_context_data(**kwargs)
        siedlung_pk = self.kwargs.get('siedlung_pk')
        context['siedlung'] = get_object_or_404(Siedlung, pk=siedlung_pk)
        return context


class ObjektDetail(DetailView):
    model = Objekt
    template_name = 'siedlungsmanager/objekt_detail.html'

    def get_object(self, **kwargs):
        """
        Overrides the default get_object method.
        Returns the object the view is displaying.
        """
        # Extract the parameters from the URL
        objekt_pk = self.kwargs.get('objekt_pk')

        # Fetch the object using the parameters
        return get_object_or_404(Objekt, pk=objekt_pk)

    def get_context_data(self, **kwargs):
        """
        Overrides the default get_context_data
        This method is used to add extra context data to the template.
        It retrieves the Siedlung object using the primary key from the URL.
        It adds this Siedlung object to the context, making it available in the template.
        """
        context = super().get_context_data(**kwargs)
        siedlung_pk = self.kwargs.get('siedlung_pk')
        context['siedlung'] = get_object_or_404(Siedlung, pk=siedlung_pk)
        return context


class ObjektUpdate(UpdateView):
    model = Objekt
    template_name = 'siedlungsmanager/objekt_update.html'
    form_class = ObjektForm

    def get_object(self, **kwargs):
        objekt_pk = self.kwargs.get('objekt_pk')
        return get_object_or_404(Objekt, pk=objekt_pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        siedlung_pk = self.kwargs.get('siedlung_pk')
        context['siedlung'] = get_object_or_404(Siedlung, pk=siedlung_pk)
        return context

    def get_success_url(self):
        kwargs = {
            'siedlung_pk': self.object.siedlung.pk,
            'objekt_pk': self.object.pk
        }
        return reverse_lazy('objekt_detail', kwargs=kwargs)


class ObjektDelete(DeleteView):
    model = Objekt
    template_name = 'siedlungsmanager/objekt_delete.html'

    def get_object(self, **kwargs):
        objekt_pk = self.kwargs.get('objekt_pk')
        return get_object_or_404(Objekt, pk=objekt_pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        siedlung_pk = self.kwargs.get('siedlung_pk')
        context['siedlung'] = get_object_or_404(Siedlung, pk=siedlung_pk)
        return context

    def get_success_url(self):
        kwargs = {
            'siedlung_pk': self.object.siedlung.pk,
        }
        return reverse_lazy('siedlung_detail', kwargs=kwargs)
