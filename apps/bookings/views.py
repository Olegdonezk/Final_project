from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import PermissionDenied


from .models import Booking
from .serializers import BookingSerializer


class BookingViewSet(viewsets.ModelViewSet):

    serializer_class = BookingSerializer
    permission_classes = [
        IsAuthenticated
    ]

    def get_queryset(self):
        user = self.request.user

        if user.role == "tenant":
            return Booking.objects.filter(
                tenant=user
            )

        if user.role == "landlord":
            return Booking.objects.filter(
                listing__owner=user
            )

        return Booking.objects.none()

    def perform_create(self, serializer):

        if self.request.user.role != "tenant":
            raise PermissionDenied(
                "Только арендатор может создавать бронирования."
            )

        serializer.save(
            tenant=self.request.user
        )


    @action(
        detail=True,
        methods=["patch"],
        url_path="confirm"
    )
    def confirm(self, request, pk=None):

        booking = self.get_object()

        if booking.listing.owner != request.user:
            return Response(
                {
                    "detail": "Только владелец объявления может подтвердить бронь."
                },
                status=status.HTTP_403_FORBIDDEN
            )


        if booking.status == Booking.Status.CANCELLED:
            return Response(
                {
                    "detail": "Нельзя подтвердить отменённую бронь."
                },
                status=status.HTTP_400_BAD_REQUEST
            )


        booking.status = Booking.Status.CONFIRMED
        booking.save()


        return Response(
            BookingSerializer(booking).data
        )


    @action(
        detail=True,
        methods=["patch"],
        url_path="cancel"
    )
    def cancel(self, request, pk=None):

        booking = self.get_object()


        if booking.tenant != request.user:
            return Response(
                {
                    "detail": "Только арендатор может отменить бронь."
                },
                status=status.HTTP_403_FORBIDDEN
            )


        if booking.status == Booking.Status.CANCELLED:
            return Response(
                {
                    "detail": "Бронь уже отменена."
                },
                status=status.HTTP_400_BAD_REQUEST
            )


        booking.status = Booking.Status.CANCELLED
        booking.save()


        return Response(
            BookingSerializer(booking).data
        )

    @action(
        detail=True,
        methods=["patch"],
        url_path="complete"
    )
    def complete(self, request, pk=None):

        booking = self.get_object()

        # Завершить может только владелец объявления
        if booking.listing.owner != request.user:
            return Response(
                {
                    "detail": "Только владелец объявления может завершить аренду."
                },
                status=status.HTTP_403_FORBIDDEN
            )

        # Нельзя завершить отменённую бронь
        if booking.status == Booking.Status.CANCELLED:
            return Response(
                {
                    "detail": "Нельзя завершить отменённую бронь."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # Завершение только подтверждённой брони
        if booking.status != Booking.Status.CONFIRMED:
            return Response(
                {
                    "detail": "Завершить можно только подтверждённую бронь."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        booking.status = Booking.Status.COMPLETED
        booking.save()

        return Response(
            BookingSerializer(booking).data
        )