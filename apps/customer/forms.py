from django import forms
from django.core.exceptions import ValidationError

from apps.customer.models import Customer


class CustomerRegisterForm(forms.Form):
    company_people = forms.CharField(required=True, strip=True, min_length=2,
                                     error_messages={
                                         'required': '请输入姓名',
                                         'min_length': '请输入有效姓名'
                                     })
    company_tele = forms.CharField(required=True, strip=True, min_length=11, max_length=11,
                                   error_messages={'required': '请输入手机号',
                                                   'min_length': '请输入有效的手机号',
                                                   'max_length': '请输入有效的手机号'})
    company_name = forms.CharField(required=True, strip=True, min_length=2,
                                   error_messages={
                                       'required': '请输入公司名',
                                       'min_length': '请输入有效的公司名'
                                   })

    def clean_company_tele(self):
        tel = self.cleaned_data['company_tele']
        if Customer.objects.filter(contact_mobile=tel).exists():
            raise ValidationError("手机号已经存在")
        return tel

