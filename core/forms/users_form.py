import re
import random
import uuid
import string

from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import PasswordResetForm, UserCreationForm

from django.db.models import Q
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from core.models import User, Cards

class CustomUserCreationForm(forms.ModelForm):

    # def __init__(self, cards=None, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     print('---------------------------------- kwargs >>> '+ str(kwargs))

    cards = tuple([(i.id, 'Карта: {0}. Доход от предложения: {1}%. Бинарный доход: {2}%'.format(i.name, i.offer_profit, i.binnary_profit)) for i in Cards.objects.filter(is_active=True)])

    password1 = forms.CharField(label=_('Пароль'), max_length=100, required=True, widget=forms.TextInput({
        # 'class': 'form-control',
        'type': 'password',
        'placeholder': _('пароль'),
    }))
    cart_number = forms.CharField(label=_('Номер карты'), max_length=200, required=True, widget=forms.TextInput({
        # 'class': 'form-control',
        'placeholder': _('номер карты'),
    }))
    first_name = forms.CharField(label=_('Имя'), max_length=200, required=True, widget=forms.TextInput({
        # 'class': 'form-control',
        'placeholder': _('имя'),
    }))
    last_name = forms.CharField(label=_('Фамилия'), max_length=200, required=True, widget=forms.TextInput({
        # 'class': 'form-control',
        'placeholder': _('фамилия'),
    }))
    date_birth = forms.CharField(label=_('Дата рождения'), max_length=200, required=True, widget=forms.TextInput({
        # 'class': 'form-control',
        'placeholder': _('дата рождения (дд.мм.ггг)'),
    }))
    place_birth = forms.CharField(label=_('Место рождения'), required=True, widget=forms.Textarea({
        # 'class': 'form-control',
        'placeholder': _('место рождения'),
    }))
    passport_series = forms.CharField(label=_('Серия паспорта'), max_length=200, required=True, widget=forms.TextInput({
        # 'class': 'form-control',
        'placeholder': _('серия паспорта'),
    }))
    registration_office = forms.CharField(label=_('Офис регистрации'), required=True, widget=forms.Textarea({
        # 'class': 'form-control',
        'placeholder': _('офис регистрации'),
    }))
    cart_type = forms.CharField(label=_('Тип карты'), required=True, widget=forms.Select(choices=cards))

    refer = forms.CharField(label=_('Пригласивший юзер (id биннара или логин)'), required=True, widget=forms.TextInput({
        # 'class': 'form-control',
        'placeholder': _('Пригласивший юзер'),
    }))
    image = forms.FileField(label=_('Изображение профиля'), required=False, )

    class Meta:
        model = User
        # field_classes = {'username': UsernameField}
        fields = ("cart_number", "password1", "first_name", "last_name", "date_birth", "place_birth", "passport_series", "registration_office", "cart_type", "refer", "image", )

    def save(self, commit=True):
        user = super(CustomUserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        login = 'uz'+uuid.uuid4().hex[:11]
        user.login = login
        user.username = login
        user.ref_id = ''.join(random.choice(string.digits) for _ in range(7))
        if commit:
            user.save()
        return user

    def clean_password1(self):
        try:
            password_validation.validate_password(self.cleaned_data['password1'])
        except forms.ValidationError as error:
            for e in error.error_list:
                self.password_alert.append(e.code)

        if len(self.cleaned_data['password1']) < 3:
            raise forms.ValidationError(
                _('Введённый пароль слишком короткий. Он должен содержать как минимум 3 символа.'))
        return self.cleaned_data['password1']

    def clean_cart_number(self):
        cart_number = self.cleaned_data.get('cart_number')
        cart_number = cart_number.replace('-', '').replace(' ', '')
        if re.findall('([0-9]{9,19})', cart_number):
            return cart_number
        self.add_error('cart_number', _('Введите корректный номер карты'))

    def clean_cart_type(self):
        cart_type = self.cleaned_data.get('cart_type')
        try:
            card = Cards.objects.get(id=cart_type)
            if card.is_active:
                return card
        except:
            pass
        self.add_error('cart_type', _('Ошибка при выборе типа карты'))

    def clean_date_birth(self):
        date_birth = self.cleaned_data.get('date_birth').strip().replace(' ', '')
        try:
            pattern = r'([0-9]{1,2}).([0-9]{1,2}).([0-9]{4})' #'дд.мм.ггг'
            if len(re.findall(pattern, date_birth)) == 1:
                date_birth = [int(i) for i in date_birth.split('.')]
                date = timezone.datetime(year=date_birth[2], month=date_birth[1], day=date_birth[0]).date()
                return date
        except:
            pass
        self.add_error('date_birth', _('Введите дату в правильном формате (дд.мм.ггг)'))

    def clean_passport_series(self):
        passport_series = self.cleaned_data.get('passport_series').replace(' ', '')
        pattern = r'[0-9]{10}'
        if len(re.findall(pattern, passport_series)) == 1:
            return passport_series
        self.add_error('passport_series', _('Введите корректный номер паспорта'))

    def clean_refer(self):
        # Проверя по полям login, ref_id
        refer = self.cleaned_data.get('refer').strip()
        print('---------------------refer >>>>>. ' + str(refer))
        try:
            referer = User.objects.filter(Q(ref_id=refer) | Q(login=refer)).first()
            if User.objects.filter(refer_id=referer.id).count() <= 2:
                return referer
            else:
                self.add_error('refer', _('У данного пользователя превышен лимит приглашений'))
        except:
            self.add_error('refer', _('Пользователь не найден'))


    def clean_image(self):
        img = self.cleaned_data['image']
        if img:
            try:
                if img.name.split('.')[-1] not in ('jpg', 'png'):
                    self.add_error('image', _('Формат изображения должен быть jpg или png'))
            except:
                raise self.add_error('image', _('Ошибка загрузки изображения.'))
            if img.size > 5 * 1024 * 1024:
                self.add_error('image', _('Размер загружаемого файла должен быть до 5Mb'))
            if 'image' not in self.errors:
                return img

    def clean(self):
        cleaned_data = super(CustomUserCreationForm, self).clean()
        print('cleaned_data >>>>>>>. ' + str(cleaned_data))
        return cleaned_data
