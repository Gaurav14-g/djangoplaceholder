from rest_framework import viewsets, filters
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from api.UserProfile.model import UserProfile
from api.UserProfile.serializer import UserProfileSerializer
from api.permissions import CustomPermission
from django.contrib.auth.models import User


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [AllowAny]
    lookup_field = 'user'

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = [
        'gender',
        'first_language',
        'country_id',
        'country_of_citizenship_id',
        'country_of_birth_id',
        'is_Indigenous',
    ]
    search_fields = [
        'user__first_name',
        'user__last_name',
        'preferred_name',
        'previous_last_name',
        'mailing_address',
        'phone_no',
    ]

    def perform_create(self, serializer):
        user_id = self.request.data.get("user")

        if user_id:
            try:
                user_obj = User.objects.get(id=user_id)
            except User.DoesNotExist:
                raise ValidationError({"user": "User does not exist."})
        else:
            user_obj = self.request.user

        if UserProfile.objects.filter(user=user_obj).exists():
            raise ValidationError({"detail": "UserProfile for this user already exists."})

        serializer.save(user=user_obj)

    def get_queryset(self):
        if self.action in ['retrieve', 'update', 'partial_update', 'destroy']:
            return UserProfile.objects.all()

        user_id = self.request.query_params.get("user_id", None)

        if self.request.user.is_authenticated and self.request.user.is_superuser:
            if user_id:
                return UserProfile.objects.filter(user__id=user_id)
            return UserProfile.objects.all()

        if self.request.user.is_authenticated:
            if user_id:
                return UserProfile.objects.filter(user__id=user_id, user=self.request.user)
            return UserProfile.objects.filter(user=self.request.user)

        return UserProfile.objects.none()