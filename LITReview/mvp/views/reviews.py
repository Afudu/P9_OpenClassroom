from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.views.generic import (
    CreateView,
    UpdateView,
    DeleteView
)
from mvp.models import Ticket, Review
from mvp.forms import TicketForm, ReviewForm


class ReviewExistingTicketCreateView(LoginRequiredMixin, FormView):
    """	Creates a review in response to an existing ticket."""

    template_name = 'reviews/create_review_from_existing_ticket.html'
    form_class = ReviewForm
    success_url = reverse_lazy('feed')

    def form_valid(self, form, **kwargs):
        """If the form is valid, redirect to the supplied URL."""
        form.instance.user = self.request.user
        form.instance.ticket = Ticket.objects.get(id=self.kwargs['existing_ticket_id'])
        form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        existing_ticket_id = self.kwargs['existing_ticket_id']
        existing_ticket = Ticket.objects.get(id=existing_ticket_id)
        context['link_name'] = 'create_existing_ticket_review'
        context['existing_ticket_review_form'] = self.get_form()
        context['existing_ticket'] = existing_ticket
        return context


class ReviewAndTicketCreateView(LoginRequiredMixin, CreateView):
    """	Creates a ticket and a review in one-step process."""

    template_name = 'reviews/create_review_and_ticket.html'

    def get(self, request, *args, **kwargs):
        ticket_form = TicketForm()
        review_form = ReviewForm()
        return render(request, self.template_name, {
            'ticket_form': ticket_form,
            'review_form': review_form,
        })

    def post(self, request, *args, **kwargs):
        ticket_form = TicketForm(request.POST, request.FILES)
        review_form = ReviewForm(request.POST)
        if ticket_form.is_valid() and review_form.is_valid():
            # ticket instance
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.save()

            # review instance
            review = review_form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()
            return redirect('feed')
        return render(request, self.template_name, {
            'ticket_form': ticket_form,
            'review_form': review_form,
        })


class ReviewUpdateView(LoginRequiredMixin, UpdateView):
    """	Updates an existing review."""
    model = Review
    form_class = ReviewForm
    template_name = 'reviews/update_review.html'
    success_url = reverse_lazy('posts')

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


class ReviewDeleteView(LoginRequiredMixin, DeleteView):
    """	Deletes an existing review."""
    model = Review
    template_name = 'reviews/delete_review.html'
    success_url = reverse_lazy('posts')

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)
