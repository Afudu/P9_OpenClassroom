from django.urls import path
from mvp.views.registration import SignUpView, CustomLoginView, CustomLogoutView
from mvp.views.feeds import HomePageView, FeedPageView
from mvp.views.posts import PostsPageView
from mvp.views.follows import FollowingListView, UserFollowView, UserUnfollowView
from mvp.views.tickets import TicketCreateView, TicketUpdateView, TicketDeleteView
from mvp.views.reviews import (
    ReviewExistingTicketCreateView,
    ReviewAndTicketCreateView,
    ReviewUpdateView,
    ReviewDeleteView
)

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('feed/', FeedPageView.as_view(), name='feed'),
    path('posts/', PostsPageView.as_view(), name='posts'),
    path('following/', FollowingListView.as_view(), name='user_following'),
    path('follow/', UserFollowView.as_view(), name="user_follow"),
    path('unfollow/<int:followed_user_id>/', UserUnfollowView.as_view(), name='user_unfollow'),
    path('ticket/create/', TicketCreateView.as_view(), name="ticket_create"),
    path('ticket/update/<int:pk>/', TicketUpdateView.as_view(), name='ticket_update'),
    path('ticket/delete/<int:pk>/', TicketDeleteView.as_view(), name='ticket_delete'),
    path('review/ticket_id_<int:existing_ticket_id>/create/', ReviewExistingTicketCreateView.as_view(),
         name='create_existing_ticket_review'),
    path('review/create/', ReviewAndTicketCreateView.as_view(), name='review_and_ticket_create'),
    path('review/update/<int:pk>/', ReviewUpdateView.as_view(), name='review_update'),
    path('review/delete/<int:pk>/', ReviewDeleteView.as_view(), name='review_delete'),
]
