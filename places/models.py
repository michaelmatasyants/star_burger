from django.db import models
from django.utils import timezone


class Place(models.Model):
    '''All places from project'''
    address = models.CharField(verbose_name='Адрес',
                               max_length=250)
    lat = models.FloatField(verbose_name='Широта',
                            blank=True)
    lon = models.FloatField(verbose_name='Долгота',
                            blank=True)
    update_date = models.DateField(verbose_name='Дата обновления',
                                   default=timezone.now,
                                   db_index=True)

    class Meta:
        verbose_name = 'Место'
        verbose_name_plural = 'Места'

    def __str__(self):
        return self.address
