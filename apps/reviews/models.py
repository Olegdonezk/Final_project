from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class Review(models.Model):

    booking = models.OneToOneField(
        "bookings.Booking",
        on_delete=models.PROTECT,
        related_name="review",
        verbose_name=_("Бронирование")
    )

    rating = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ],
        verbose_name=_("Оценка")
    )

    comment = models.TextField(
        verbose_name=_("Комментарий")
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Дата создания")
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Дата обновления")
    )


    class Meta:
        verbose_name = _("Отзыв")
        verbose_name_plural = _("Отзывы")
        ordering = ["-created_at"]

    def clean(self):
        if self.booking.status != "completed":
            raise ValidationError(
                _("Отзыв можно оставить только после завершения аренды.")
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return (
            f"{self.booking.tenant.email} → "
            f"{self.booking.listing.title} "
            f"({self.rating}/5)"
        )