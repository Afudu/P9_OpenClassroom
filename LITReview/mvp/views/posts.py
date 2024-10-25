from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from mvp.models import Ticket, Review


class PostsPageView(LoginRequiredMixin, generic.TemplateView):
    """View handling the posts page: displays logged-in user's tickets and reviews."""

    template_name = 'posts/posts.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # current_user
        current_user = self.request.user

        # own tickets
        own_tickets = Ticket.objects.filter(user=current_user)

        # own reviews
        own_reviews = Review.objects.filter(user=current_user)

        context['link_name'] = 'posts_page'
        context['own_tickets'] = own_tickets
        context['own_reviews'] = own_reviews
        return context
