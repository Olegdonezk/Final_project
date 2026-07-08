from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _




class SearchHistory(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='search_history',
        verbose_name=_('Пользователь')
    )
    query_text = models.CharField(max_length=255, verbose_name=_('Поисковый запрос'))
    searched_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Дата запроса'))

    class Meta:
        verbose_name = _('История поиска')
        verbose_name_plural = _('История поиска')
        ordering = ['-searched_at']


class ViewHistory(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='view_history',
        verbose_name=_('Пользователь')
    )
    listing = models.ForeignKey(
        "listings.Listing",
        on_delete=models.CASCADE,
        related_name='views_history',
        verbose_name=_('Объявление')
    )
    viewed_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Дата просмотра'))

    class Meta:
        verbose_name = _('История просмотра')
        verbose_name_plural = _('История просмотров')
        ordering = ['-viewed_at']