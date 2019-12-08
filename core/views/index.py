import os
import json
import string
import random

from datetime import datetime
from django.db.models import Q
from django.conf import settings
from django.views import generic
from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect, render_to_response, get_object_or_404


class IndexView(generic.View):

    def get(self, request, *args, **kwargs):
        context = {
            'test':'ZAEBUMBA!!!!!!!!!!!!!!!'
        }

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
