import random
from datetime import timedelta
from decimal import Decimal

from django.utils import timezone
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from GoTrain.utils.sms import send_sms
from profiles.api.serializers.profiles import ProfileListSerializer, ProfileRetrieveSerializer, ProfileUpdateSerializer
from profiles.models import Profile
from profiles.models.phone import PhoneVerification


class ProfilesViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    GenericViewSet,
):
    qs = Profile.objects.all()

    def get_queryset(self):
        if self.action == "retrieve":
            return self.qs.filter(user=self.request.user)
        return self.qs

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_permissions(self):
        if self.action == "list":
            return [IsAdminUser()]
        return [IsAuthenticated()]

    def get_serializer_class(self):
        if self.action == "list":
            return ProfileListSerializer
        if self.action == "retrieve":
            return ProfileRetrieveSerializer
        return ProfileUpdateSerializer

    @action(detail=False, methods=["get", "patch"], url_path="me")
    def me(self, request):
        profile = Profile.objects.get(user=request.user)
        if request.method == "PATCH":
            serializer = ProfileUpdateSerializer(
                profile,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        serializer = ProfileRetrieveSerializer(profile)
        return Response(serializer.data)

    @action(detail=False, methods=["post"], url_path="top-up")
    def top_up(self, request):
        amount = request.data.get("amount")
        if not amount or float(amount) <= 0:
            return Response(
                {"detail": "Amount must be positive."},
                status=status.HTTP_400_BAD_REQUEST
            )
        profile = request.user.profile
        profile.balance += Decimal(amount)
        profile.save(update_fields=["balance"])
        return Response({"balance": profile.balance})

    @action(detail=False, methods=["post"], url_path="phone/send-code")
    def send_code(self, request):
        phone_number = request.data.get("phone_number")
        code = str(random.randint(100000, 999999))
        expires_at = timezone.now() + timedelta(minutes=10)

        PhoneVerification.objects.update_or_create(
            profile=request.user.profile,
            defaults={
                "phone_number": phone_number,
                "code": code,
                "is_verified": False,
                "expires_at": expires_at,
            }
        )

        # відправити SMS через Twilio
        send_sms(phone_number, f"Your verification code: {code}")

        return Response({"detail": "Code sent."})

    @action(detail=False, methods=["post"], url_path="phone/verify")
    def verify_code(self, request):
        code = request.data.get("code")

        try:
            verification = request.user.profile.phone_verification
        except PhoneVerification.DoesNotExist:
            return Response(
                {"detail": "No verification request found."},
                status=status.HTTP_404_NOT_FOUND
            )

        if verification.is_expired():
            return Response(
                {"detail": "Code expired."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if verification.code != code:
            return Response(
                {"detail": "Invalid code."},
                status=status.HTTP_400_BAD_REQUEST
            )

        verification.is_verified = True
        verification.save(update_fields=["is_verified"])

        # зберігаємо номер в профіль
        profile = request.user.profile
        profile.phone_number = verification.phone_number
        profile.save(update_fields=["phone_number"])

        return Response({"detail": "Phone verified successfully."})
