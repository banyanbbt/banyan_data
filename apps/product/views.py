from django.shortcuts import render
from django.http.response import JsonResponse
from django.views.generic.base import View

from apps.util.decorate import login_required
from apps.util.wrapper import current_user
from django.utils.decorators import method_decorator

from apps.product.models import AccountProduct
from apps.customer.models import Customer

class ProductHome(View):

    def get(self, request):
        return render(request, 'product/index.html')


class AccountProductDataView(View):

    @method_decorator(login_required)
    def get(self, request):
        user = current_user(request)
        products = []
        if user and user.is_company():
            customer = Customer.find_by_id(user.customer_id)
            if customer:
                products = AccountProduct.list_user_products(customer.gateway_account)
        return JsonResponse({'products': products})

