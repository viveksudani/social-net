from datetime import timedelta
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.db.models import Q
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view
from rest_framework.response import Response


from core.serializers import UserSerializer, FriendRequestSerializer
from core.models import FriendRequest
from core.pagination import AppPagination


User = get_user_model()


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system."""

    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]


class PendingRequestListView(generics.ListAPIView):
    """List received pending request"""

    pagination_class = AppPagination
    serializer_class = FriendRequestSerializer
    queryset = FriendRequest.objects.all()

    def get_queryset(self):
        return self.queryset.filter(receiver=self.request.user, status="Pending")


class FriendsListView(generics.ListAPIView):
    """List Friends (accepted)"""

    pagination_class = AppPagination
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_queryset(self):
        return self.queryset.filter(id__in=self.request.user.friends.all())


class SearchUsersListView(generics.ListAPIView):
    """Seach Other users by name or email"""

    pagination_class = AppPagination
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_queryset(self):
        search_key = self.request.GET.get("search")
        if search_key:
            self_id = self.request.user.id
            queryset = self.queryset.exclude(id=self_id).filter(
                Q(first_name__icontains=search_key)
                | Q(last_name__icontains=search_key)
                | Q(email=search_key)
            )

        else:
            queryset = User.objects.none()

        return queryset


@api_view(["POST"])
def send_friend_request(request):
    """Send Friend request to an user if already not sent."""

    try:
        receiver_id = int(request.POST["receiver_id"])
    except:
        response = {"detail": "'receiver_id' is required and must be integer."}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    # Validate Receiver ID is valid
    try:
        receiver = User.objects.exclude(id=request.user.id).get(id=receiver_id)
    except User.DoesNotExist:
        response = {"detail": f"Invalid 'receiver_id'."}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    # Check if reciever is already in friend list
    friends_list = list(request.user.friends.values_list("id", flat=True))
    if receiver_id in friends_list:
        response = {"detail": f"Receiver is already in friend list."}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    # Check if User has sent 3 requests in last 1 minute.
    ten_minutes_ago = timezone.now() - timedelta(minutes=1)
    count = FriendRequest.objects.filter(created_at__gte=ten_minutes_ago).count()
    if count >= 3:
        return Response(
            {
                "detail": f"Can not process more than 3 requests per minute. Please try after sometime."
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    _, created = FriendRequest.objects.get_or_create(
        sender=request.user, receiver=receiver, status="Pending"
    )
    if not created:
        return Response(
            {"detail": f"Friend Request to this friend already exist."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    return Response({"detail": "Friend Request Sent."}, status=status.HTTP_200_OK)


@api_view(["POST"])
def process_friend_request(request):
    """Accept or Reject friend request"""

    try:
        friend_request_id = request.POST["friend_request_id"]
        action = request.POST["action"]
    except KeyError:
        response = {"detail": "'friend_request_id' and 'action' are required inputs."}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    # validate action
    if not action in ["accept", "reject"]:
        response = {
            "detail": "invalid 'action', valid options are 'accept' and 'reject'."
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    # Validate request_id is valid
    try:
        friend_request = FriendRequest.objects.get(
            id=friend_request_id, receiver=request.user.id, status="Pending"
        )
    except FriendRequest.DoesNotExist:
        response = {"detail": f"Invalid 'request_id'."}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    if action == "accept":
        friend_request.status = "Accepted"
        message = "Friend Request Accepted"
    else:
        friend_request.status = "Rejected"
        message = "Friend Request Rejected"

    friend_request.save()

    # Add sender to friends list
    request.user.friends.add(friend_request.sender)

    return Response({"detail": message}, status=status.HTTP_200_OK)
