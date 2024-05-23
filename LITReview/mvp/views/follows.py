from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic import FormView
from mvp.models import User, UserFollows
from mvp.forms import UserFollowForm


class FollowingListView(LoginRequiredMixin, FormView):
    """View to list the users that the current user follows."""

    template_name = 'follows/following.html'
    form_class = UserFollowForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_user = self.request.user
        context.update({
            'link_name': 'following_page',
            'user_following_list': current_user.following.all(),
            'user_followers_list': current_user.followers.all(),
            'user_follow_form': self.get_form()
        })
        return context


class UserFollowView(LoginRequiredMixin, FormView):
    """View handling following of another user."""

    def post(self, request, *args, **kwargs):
        current_user = self.request.user
        submitted_username = request.POST['followed_user']
        try:
            submitted_user = User.objects.get(username=submitted_username)
            if submitted_user == current_user:
                messages.error(self.request, "You cannot follow yourself.")
            elif UserFollows.objects.filter(user=current_user, followed_user=submitted_user).exists():
                messages.error(self.request, f"You are already following {submitted_user}.")
            else:
                UserFollows.objects.create(user=current_user, followed_user=submitted_user)
                messages.success(self.request, f"You are now following {submitted_user}.")
        except User.DoesNotExist:
            messages.error(self.request, f"User {submitted_username} does not exist.")
        return redirect('user_following')


class UserUnfollowView(LoginRequiredMixin, FormView):
    """View handling unfollowing of another user."""

    def post(self, request, *args, **kwargs):
        current_user = self.request.user
        followed_user_id = self.kwargs.get('followed_user_id')
        followed_user = User.objects.get(id=followed_user_id)
        user_follows_instance = UserFollows.objects.get(user=current_user, followed_user_id=followed_user_id)
        user_follows_instance.delete()
        messages.success(request, f"You have now unfollowed {followed_user}.")
        return redirect('user_following')
