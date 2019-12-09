import os
import uuid
import random
import string

from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from .abstract_user import validate_img, CustomAbstractUser


class Cards(models.Model):

    class Meta:
        verbose_name = 'Модель для карт'
        verbose_name_plural = 'Модели для карт'

    name = models.CharField(max_length=200, verbose_name='Название карты')
    offer_profit = models.IntegerField(verbose_name='Доход от предложения')
    binnary_profit = models.IntegerField(verbose_name='Бинарный доход')
    is_active = models.BooleanField(default=True, verbose_name='Доступна ли карта')

    def __str__(self):
        return self.name

    def get_name(self):
        return 'Карта: {0}. Доход от предложения: {1}%. Бинарный доход: {2}%'.format(self.name, self.offer_profit, self.binnary_profit)


class User(CustomAbstractUser):

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    cart_number = models.CharField(max_length=20, verbose_name='Номер карты',)
    date_birth = models.DateField(null=True, verbose_name='Дата рождения',)
    place_birth = models.TextField(null=True, verbose_name='Место рождения',)
    passport_series = models.CharField(max_length=20, null=True, verbose_name='Серия паспорта',)
    registration_office = models.TextField(null=True, verbose_name='Офис регистрации')
    cart_type = models.ForeignKey(Cards, on_delete=models.DO_NOTHING, null=True, verbose_name='Тип карты')
    refer = models.ForeignKey('self', on_delete=models.DO_NOTHING, null=True, verbose_name='Пригласивший юзер')  # 13: ID бинара(за кем они находятся)  ????
    ref_id = models.CharField(max_length=20, null=True, unique=True, verbose_name='Код бинара для приглашения новых юзеров')
    image = models.ImageField(null=True, upload_to='images/profiles/', validators=[validate_img], verbose_name='Изображение профиля')

    def __str__(self):
        return self.login

    # def image_path(self):
    #     return '{0}profiles/{1}'.format(settings.UPLOAD_IMAGES_PATH, self.image)