from django.shortcuts import render
from django.http.response import JsonResponse
from django.views.generic.base import View

from apps.customer.models import Customer
from apps.billing.models import BillMonthly

from apps.util.decorate import login_required
from apps.util.wrapper import current_user
from django.utils.decorators import method_decorator


class BillingHome(View):

    @method_decorator(login_required)
    def get(self, request):
        return render(request, 'billing/index.html')


class AccountBillDataView(View):

    @method_decorator(login_required)
    def get(self, request):
        user = current_user(request)
        resp = dict()

        year = request.GET.get('year')
        month = request.GET.get('month')
        week = request.GET.get('week')

        if user and user.is_company():
            customer = Customer.find_by_id(user.customer_id)
            if customer:
                resp['summary'], resp['billing'] = BillMonthly.construct_bill_dict(year, month, week, customer.gateway_account)

        return JsonResponse(resp)

