from django import forms
from django.forms import fields
from django.forms import widgets
from django.core.validators import RegexValidator


class WithdrawForm(forms.Form):
    """提现"""

    bbn_count = fields.IntegerField(label="提现BBN数量",
                                    required=True,
                                    min_value=0,
                                    widget=widgets.NumberInput(attrs={"class": "form-control",
                                                                      "id": "withdraw_count",
                                                                      "placeholder": "请输入要提现的数量(必须为100的整数倍)",
                                                                      "required": False,
                                                                      }),
                                    error_messages={'required': '提现数量不能为空',
                                                    'invalid': '请输入100的整数倍的数字'})

    wallet_address = fields.CharField(label="提现地址",
                                      required=True,
                                      strip=True,
                                      widget=widgets.TextInput(attrs={"class": "form-control",
                                                                      "id": "withdraw_address",
                                                                      "placeholder": "请输入提现地址",
                                                                      "required": False,
                                                                      }),
                                      max_length=42,
                                      min_length=42,
                                      validators=[RegexValidator(r'^0x[0-9A-Za-z]{40}$', '地址无效')],
                                      error_messages={
                                          'required': '地址不能为空',
                                          'min_length': '请输入有效的地址',
                                          'max_length': '请输入有效的地址'
                                      })

