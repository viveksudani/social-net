from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from core import views

app_name = "core"

urlpatterns = [
    path("signup/", views.CreateUserView.as_view(), name="signup"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("send-friend-request/", views.send_friend_request, name="send_friend_request"),
    path(
        "process-friend-request/",
        views.process_friend_request,
        name="process_friend_request",
    ),
    path("friends/", views.FriendsListView.as_view(), name="friends"),
    path(
        "pending-friend-requests/",
        views.PendingRequestListView.as_view(),
        name="pending_friend_requests",
    ),
    path("search-users/", views.SearchUsersListView.as_view(), name="search"),
]
