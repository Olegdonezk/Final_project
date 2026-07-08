from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _


class Listing(models.Model):
    class HousingTypes(models.TextChoices):
        APARTMENT = 'apartment', _('Квартира')
        HOUSE = 'house', _('Дом')
        STUDIO = 'studio', _('Студия')
        ROOM = 'room', _('Комната')

    # Связь с арендодателем
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='listings',
        verbose_name=_('Арендодатель')
    )

    # Основная информация
    title = models.CharField(max_length=255, verbose_name=_('Заголовок'))
    description = models.TextField(verbose_name=_('Описание'))
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.0)],
        verbose_name=_('Цена за месяц (EUR)')
    )
    rooms = models.PositiveSmallIntegerField(verbose_name=_('Количество комнат'))
    housing_type = models.CharField(
        max_length=20,
        choices=HousingTypes.choices,
        default=HousingTypes.APARTMENT,
        verbose_name=_('Тип жилья')
    )

    # Локация (Германия)
    city = models.CharField(max_length=100, verbose_name=_('Город (Германия)'))
    district = models.CharField(max_length=100, blank=True, verbose_name=_('Район'))
    address = models.CharField(max_length=255, verbose_name=_("Адрес"))

    # Статус доступности и счетчик просмотров (для популярности)
    is_active = models.BooleanField(default=True, verbose_name=_('Активно'))
    views_count = models.PositiveIntegerField(default=0, verbose_name=_('Количество просмотров'))

    # Таймстампы
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Дата добавления'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Дата обновления'))

    class Meta:
        verbose_name = _('Объявление')
        verbose_name_plural = _('Объявления')
        ordering = ['-created_at']
        # Индексы для оптимизации поиска и фильтрации в MySQL
        indexes = [
            models.Index(fields=['price']),
            models.Index(fields=['rooms']),
            models.Index(fields=['city']),
            models.Index(fields=['is_active']),
        ]

    def __str__(self):
        return f"{self.title} ({self.city}) — {self.price} EUR"


