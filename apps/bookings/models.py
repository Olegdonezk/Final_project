from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from apps.listings.models import Listing


class Booking(models.Model):

    class Status(models.TextChoices):
        PENDING = "pending", _("Ожидает подтверждения")
        CONFIRMED = "confirmed", _("Подтверждено")
        CANCELLED = "cancelled", _("Отменено")
        COMPLETED = "completed", "Завершена"

    tenant = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="bookings",
        verbose_name=_("Арендатор")
    )

    listing = models.ForeignKey(
        Listing,
        on_delete=models.CASCADE,
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


    def __str__(self):
        return (
            f"{self.tenant.email} → "
            f"{self.listing.title}"
        )