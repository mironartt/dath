import os
import json
import string
import random

from datetime import datetime
from django.db.models import Q
from django.conf import settings
from django.views import generic
from django.contrib import auth
from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect, render_to_response, get_object_or_404
from core.models import User, Cards
from core.forms.users_form import CustomUserCreationForm


class IndexView(generic.View):

    def get(self, request, *args, **kwargs):
        context = {}

        return render(request, 'core/index.html', context)


def request_ajax(request, *args, **kwargs):

    def Ajax404(text = ''):
        response_data = {
            'type': 'error',
            'errortext': str(text),
            'response_dict': {},
        }
        return HttpResponse(json.dumps(response_data), content_type="application/json")

    if request.method == 'POST':
        if request.POST['key'] == 'subscribe':
            response_data = {
                'type': 'success',
                'key': 'subscribe',
                'response_dict': {},
            }
            return HttpResponse(json.dumps(response_data), content_type='application/json')

    return Ajax404('Требуется авторизация')


class RegisterFormView(generic.CreateView):
    form_class = CustomUserCreationForm
    template_name = 'registration/registration.html'

    def dispatch(self, request, *args, **kwargs):
        # if request.user.is_authenticated and not kwargs:
        #     return redirect('index')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        context = {
            'form': self.form_class(),
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        context = {}
        if request.method == 'POST':
            form = self.form_class(request.POST, request.FILES)
            context['form'] = form
            if form.is_valid():
                print('YES!!!!!!!!!! form >>> ' + str())
                user = form.save()
                auth.login(request, user)
                return redirect('profile')
        return render(request, self.template_name, context)


class ProfileView(generic.View):
    template_name = 'core/profile.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        context = {}
        return render(request, self.template_name, context)


def logout_view(request, *args, **kwargs):
    if request.user.is_authenticated:
        auth.logout(request)
    return redirect('index')


def login_view(request, *args, **kwargs):
    if request.user.is_authenticated:
        return redirect('profile')
    elif request.method == 'GET':
        return render(request, "registration/login.html", )
    elif request.method == 'POST':
        form_auth = auth.forms.AuthenticationForm(request=request, data=request.POST)
        if form_auth.is_valid():
            user = form_auth.get_user()
            auth.login(request, user)
            return redirect('profile')
    else:
        form_auth = auth.forms.AuthenticationForm()
    return render(request, "registration/login.html", {'form_auth': form_auth})

