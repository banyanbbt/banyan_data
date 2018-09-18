from django import forms
from apps.cooperation.models import DataSourceCooperationInfo
from apps.util.sms import data_source_cooperation_template


class DataSourceCooperationForm(forms.Form):

    desc = forms.CharField(required=True,
                           error_messages={"required": "数据描述不能为空哦"})

    data_num = forms.IntegerField(required=False)
    data_field = forms.CharField(required=False)
    contact_name = forms.CharField(required=True, max_length=255, min_length=2,
                                   error_messages={"required": "姓名不能为空哦",
                                                   "max_length": "姓名不合法哦",
                                                   "min_length": "姓名不合法哦"})
    contact_mobile = forms.CharField(required=True, max_length=11,  min_length=11,
                                     error_messages={"required": "手机号不能为空哦",
                                                     "max_length": "手机号不合法哦",
                                                     "min_length": "手机号不合法哦"})

    def save(self):
        instance = dict()
        instance['desc'] = self.cleaned_data.get('desc')
        instance['contact_name'] = self.cleaned_data.get('contact_name')
        instance['contact_mobile'] = self.cleaned_data.get('contact_mobile')
        if 'data_num' in self.cleaned_data:
            instance['data_amount'] = self.cleaned_data.get('data_num')
        if 'data_field' in self.cleaned_data:
            instance['data_fields'] = self.cleaned_data.get('data_field')

        DataSourceCooperationInfo.objects.create(**instance)

    def build_up_remind_email_text_content(self):
        desc = self.cleaned_data.get('desc')
        data_num = self.cleaned_data.get('data_num', '')
        data_fields = self.cleaned_data.get('data_field', '')
        contact_name = self.cleaned_data.get('contact_name')
        contact_mobile = self.cleaned_data.get('contact_mobile')

        return data_source_cooperation_template.format(desc, data_num, data_fields, contact_name, contact_mobile)


