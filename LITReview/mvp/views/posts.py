from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from itertools import chain
from django.db.models import CharField, Value
from mvp.models import Ticket, Review


class PostsPageView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'posts/posts.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # current_user
        current_user = self.request.user

        # current_user tickets
        own_tickets = Ticket.objects.filter(user=current_user)

        # Annotate as Ticket in the QuerySet: returns queryset of tickets
        own_tickets = own_tickets.annotate(content_type=Value('TICKET', CharField()))

        # own tickets not reviewed
        own_tickets_not_reviewed = own_tickets.exclude(
            id__in=[review.ticket.id for review in Review.objects.filter(ticket__in=own_tickets)]).annotate(
            ticket_status=Value('own_tickets_not_reviewed', CharField())
        )

        # own tickets reviewers - ids
        own_tickets_reviewers_ids = []
        for ticket in Ticket.objects.filter(user=current_user):
            for review in Review.objects.all():
                if review.ticket == ticket:
                    own_tickets_reviewers_ids.append(review.user.pk)

        # targeting own reviews + own tickets reviewed by followers
        reviews = (Review.objects.filter(user_id__in=[current_user.pk]) |
                   Review.objects.filter(user_id__in=own_tickets_reviewers_ids)
                   )
        # Annotate own review
        reviews = reviews.annotate(content_type=Value('REVIEW', CharField()))

        # combine and sort the two types of posts
        own_posts = sorted(
            chain(reviews, own_tickets_not_reviewed),
            key=lambda post: post.time_created, reverse=True
        )

        context['link_name'] = 'posts_page'
        context['own_posts'] = own_posts
        return context
