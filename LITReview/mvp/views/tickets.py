from django.views.generic import (
    CreateView,
    UpdateView,
    DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from mvp.forms import TicketForm
from mvp.models import Ticket


class TicketCreateView(LoginRequiredMixin, CreateView):
    model = Ticket
    template_name = 'tickets/create_ticket.html'
    form_class = TicketForm
    success_url = reverse_lazy('feed')

    def form_valid(self, form, **kwargs):
        # This method is called when valid form data has been POSTed.
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ticket_form'] = self.get_form()
        return context


class TicketUpdateView(LoginRequiredMixin, UpdateView):
    model = Ticket
    form_class = TicketForm
    template_name = 'tickets/update_ticket.html'
    success_url = reverse_lazy('posts')

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


class TicketDeleteView(LoginRequiredMixin, DeleteView):
    model = Ticket
    template_name = 'tickets/delete_ticket.html'
    success_url = reverse_lazy('posts')

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)
