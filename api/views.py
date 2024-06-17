from django.contrib.auth.models import User
import logging
from django.db.models import Q
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import FriendRequest
from .serializers import UserSerializer, FriendRequestSerializer
logger = logging.getLogger(__name__)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        request_body=UserSerializer,
        responses={201: UserSerializer, 400: 'Bad Request'}
    )
    @action(detail=False, methods=['post'], permission_classes=[permissions.AllowAny])
    def signup(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING, description='Username'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='Password')
            }
        ),
        responses={200: 'Token pair', 401: 'Invalid Credentials'}
    )
    @action(detail=False, methods=['post'], permission_classes=[permissions.AllowAny])
    def login(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = User.objects.filter(username=username).first()
        if user and user.check_password(password):
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'search',
                openapi.IN_QUERY,
                description="Search keyword for username, email, first name, or last name",
                type=openapi.TYPE_STRING
            )
        ]
    )
    @action(detail=False, methods=['get'])
    def search(self, request):
        keyword = request.query_params.get('search', '')
        if keyword:
            queryset = User.objects.filter(
                Q(username__icontains=keyword) |
                Q(email__icontains=keyword) |
                Q(first_name__icontains=keyword) |
                Q(last_name__icontains=keyword)
            )
        else:
            queryset = User.objects.none()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def friends(self, request):
        friends = User.objects.filter(
            Q(sent_requests__receiver=request.user, sent_requests__status=FriendRequest.ACCEPTED) |
            Q(received_requests__sender=request.user, received_requests__status=FriendRequest.ACCEPTED)
        ).distinct()
        page = self.paginate_queryset(friends)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(friends, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def pending_requests(self, request):
        if not request.user.is_authenticated:
            return Response({"error": "User not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)
        
        pending_requests = FriendRequest.objects.filter(receiver=request.user, status=FriendRequest.PENDING)
        
        if not pending_requests.exists():
            return Response({"message": "No pending friend requests."}, status=status.HTTP_200_OK)
        
        page = self.paginate_queryset(pending_requests)
        if page is not None:
            serializer = FriendRequestSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = FriendRequestSerializer(pending_requests, many=True)
        return Response(serializer.data)


class FriendRequestViewSet(viewsets.ModelViewSet):
    queryset = FriendRequest.objects.all()
    serializer_class = FriendRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        responses={201: FriendRequestSerializer, 400: 'Bad Request'}
    )
    @action(detail=True, methods=['post'])
    def send_request(self, request, pk=None):
        receiver = User.objects.get(pk=pk)
        friend_request, created = FriendRequest.objects.get_or_create(sender=request.user, receiver=receiver)
        if created:
            return Response(FriendRequestSerializer(friend_request).data, status=status.HTTP_201_CREATED)
        return Response({'error': 'Friend request already sent'}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'status': openapi.Schema(type=openapi.TYPE_STRING, description='Status of the friend request')
            }
        ),
        responses={200: FriendRequestSerializer, 400: 'Invalid status', 404: 'Friend request not found'}
    )
    @action(detail=True, methods=['put'])
    def update_request(self, request, pk=None):
        try:
            friend_request = FriendRequest.objects.get(id=pk, receiver=request.user)
        except FriendRequest.DoesNotExist:
            return Response({'error': 'Friend request not found or you are not authorized to update this request'}, status=status.HTTP_404_NOT_FOUND)
        
        req_status = request.data.get('status')
        if req_status in [FriendRequest.ACCEPTED, FriendRequest.REJECTED]:
            friend_request.status = req_status
            friend_request.save()
            return Response(FriendRequestSerializer(friend_request).data)

        return Response({'error': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)

    # ... other methods ...
