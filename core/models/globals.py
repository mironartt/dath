from django.db import models
from django.contrib.postgres.fields import JSONField


# class MailsSendings(models.Model):
#
#     class Meta:
#         verbose_name = 'Email подписанный на рассылку уведомлений'
#         verbose_name_plural = 'Emails подписанные на рассылку уведомлений'
#
#     email = models.EmailField(verbose_name='Email')
#     key_for_cancel = models.CharField(max_length=100, verbose_name='Ключ для сыллки отмены', null=True, unique=True)
#     is_active = models.BooleanField(default=True)
#
#     date_last_sending = models.DateTimeField(null=True, verbose_name='Дата последнего отпраления')
#
#     date_created = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
#     date_updated = models.DateTimeField(auto_now=True, verbose_name='Обновлен')
#
#     def __str__(self):
#         return self.email
