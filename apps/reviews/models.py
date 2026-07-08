from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _


class Review(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name=_("Пользователь")
    )

    listing = models.ForeignKey(
        "listings.Listing",
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name=_("Объявление")
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

        constraints = [
            models.UniqueConstraint(
                fields=["user", "listing"],
                name="unique_user_listing_review"
            )
        ]


    def __str__(self):
        return f"{self.user.email} → {self.listing.title} ({self.rating}/5)"