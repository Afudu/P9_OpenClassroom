from django.shortcuts import redirect
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from itertools import chain
from django.db.models import CharField, Value
from mvp.models import Ticket, Review, UserFollows


class HomePageView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'feeds/home.html'

    def get(self, request, **kwargs):
        return redirect('/feed/')


class FeedPageView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'feeds/feed.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # logged-in user
        current_user = self.request.user

        # Current_user's following list - ids
        current_user_following_ids = [subscription.followed_user.pk for subscription in
                                      UserFollows.objects.filter(user=current_user)]

        # current_user's tickets reviewers - ids
        current_user_ticket_reviewers_ids = []
        for ticket in Ticket.objects.filter(user=current_user):
            for review in Review.objects.all():
                if review.ticket == ticket:
                    current_user_ticket_reviewers_ids.append(review.user.pk)

        # # # Queries on tickets :
        # Own and followed users tickets.
        tickets = Ticket.objects.filter(user_id__in=[current_user.pk] + current_user_following_ids
                                        )

        # Annotate as Ticket in the QuerySet: returns queryset of tickets
        tickets = tickets.annotate(content_type=Value('TICKET', CharField()))

        # Own and followed users tickets not reviewed
        tickets_not_reviewed = tickets.exclude(
            id__in=[review.ticket.id for review in Review.objects.filter(ticket__in=tickets)]
        ).annotate(ticket_status=Value('tickets_not_reviewed', CharField()))

        # Own and followed users tickets already reviewed
        tickets_already_reviewed = tickets.filter(
            id__in=[review.ticket.id for review in Review.objects.filter(ticket__in=tickets)]).annotate(
            ticket_status=Value('tickets_already_reviewed', CharField()))

        # # # Queries on reviews :Reviews of current user, their following list and reviewers of own tickets.
        reviews = (Review.objects.filter(user_id__in=[current_user.pk]) |
                   Review.objects.filter(user_id__in=current_user_following_ids) |
                   Review.objects.filter(user_id__in=current_user_ticket_reviewers_ids)
                   )

        # Annotate review - returns queryset of reviews
        reviews = reviews.annotate(content_type=Value('REVIEW', CharField()))

        # combine and sort the two types of posts
        posts = sorted(
            chain(reviews, tickets_not_reviewed, tickets_already_reviewed),
            key=lambda post: post.time_created,
            reverse=True
        )
        # context data
        context['link_name'] = 'feed_page'
        context['posts'] = posts
        return context
