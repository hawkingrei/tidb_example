from django.http import JsonResponse, HttpResponse
from django.utils.decorators import method_decorator
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from django.db import Error, OperationalError
from django.db.transaction import atomic
from functools import wraps
import json
import sys
import time

from .models import *

def retry_on_exception(view, num_retries=3, on_failure=HttpResponse(status=500), delay_=0.5, backoff_=1.5):
    @wraps(view)
    def retry(*args, **kwargs):
        delay = delay_
        for i in range(num_retries):
            try:
                return view(*args, **kwargs)
            except Exception as e:
                return on_failure
    return retry


class PingView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse("python/django", status=200)


@method_decorator(csrf_exempt, name='dispatch')
class OrderView(View):
    def get(self, request, id=None, *args, **kwargs):
        if id is None:
            orders = list(Orders.objects.values())
        else:
            orders = list(Orders.objects.filter(id=id).values())
        return JsonResponse(orders, safe=False)


    @retry_on_exception
    @atomic
    def post(self, request, *args, **kwargs):
        form_data = json.loads(request.body.decode())
        username = form_data['username']
        price = form_data['price']
        c = Orders(username=username, price=price)
        c.save()        
        return HttpResponse(status=200)

    @retry_on_exception
    @atomic
    def delete(self, request, id=None, *args, **kwargs):
        if id is None:
            return HttpResponse(status=404)
        Orders.objects.filter(id=id).delete()
        return HttpResponse(status=200)