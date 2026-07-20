from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from apps.listings.models import Listing

from django.db.models import Q, F

from django.core.exceptions import ValidationError


class Booking(models.Model):

    class Status(models.TextChoices):
        PENDING = "pending", _("Ожидает подтверждения")
        CONFIRMED = "confirmed", _("Подтверждено")
        CANCELLED = "cancelled", _("Отменено")
        COMPLETED = "completed", "Завершена"

    tenant = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="bookings",
        verbose_name=_("Арендатор")
    )

    listing = models.ForeignKey(
        Listing,
        on_delete=models.PROTECT,
        related_name="bookings",
        verbose_name=_("Объявление")
    )

    start_date = models.DateField(
        verbose_name=_("Дата начала аренды")
    )

    end_date = models.DateField(
        verbose_name=_("Дата окончания аренды")
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
        verbose_name=_("Статус")
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Дата создания")
    )


    class Meta:
        verbose_name = _("Бронирование")
        verbose_name_plural = _("Бронирования")
        ordering = ["-created_at"]

        constraints = [
            models.CheckConstraint(
                check=Q(end_date__gt=F("start_date")),
                name="booking_end_after_start",
            ),
            models.UniqueConstraint(
                fields=[
                    "tenant",
                    "listing",
                    "start_date",
                    "end_date",
                ],
                name="unique_booking",
            ),
        ]

    def clean(self):
        overlapping = Booking.objects.filter(
            listing=self.listing,
            start_date__lt=self.end_date,
            end_date__gt=self.start_date,
        ).exclude(
            status=Booking.Status.CANCELLED
        )

        if self.pk:
            overlapping = overlapping.exclude(pk=self.pk)

        if overlapping.exists():
            raise ValidationError(
                _("На выбранные даты жилье уже забронировано.")
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return (
            f"{self.tenant.email} → "
            f"{self.listing.title}"
        )