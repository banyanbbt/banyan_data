from django.contrib.auth.hashers import check_password
from django.core.exceptions import ValidationError
from django import forms
from django.forms import fields
from django.forms import widgets
from django.core.validators import RegexValidator
from apps.user.models import UserProfile


class RegisterForm(forms.Form):
    """
    注册表单
    """
    email = fields.EmailField(label='Email',
                              required=True,
                              widget=widgets.TextInput(attrs={"id": "email2", "class": "form-control",
                                                              "placeholder": "请输入你的邮箱",
                                                              "required": False}),
                              error_messages={'required': '邮箱不能为空哦', 'invalid': '请输入正确的邮箱格式'})

    password = fields.CharField(label='Password',
                                widget=widgets.PasswordInput(attrs={"id": "password2", "class": "form-control",
                                                                    "placeholder": "请输入密码, 必须包含数字,字母",
                                                                    "required": False},
                                                             render_value=True),
                                required=True, min_length=6, max_length=20, strip=True,
                                validators=[
                                   RegexValidator(r'((?=.*\d))^.{6,20}$', '必须包含数字'),

                                   RegexValidator(r'((?=.*[a-zA-Z]))^.{6,20}$', '必须包含字母'),

                                ],
                                error_messages={
                                   'required': '密码不能为空哦',
                                   'min_length': '密码最少为6个字符',
                                   'max_length': '密码最多不超过20个字符'
                                })

    password_confirm = fields.CharField(label='Password_Confirm',
                                        widget=widgets.PasswordInput(attrs={"id": "password3", "class": "form-control",
                                                                            "placeholder": "请再次输入密码",
                                                                            "required": False},
                                                                     render_value=True),
                                        required=True,
                                        error_messages={"required": "请再次输入密码"}
                                        )

    def clean_email(self):
        """
        验证邮箱是否存在
        """
        email = self.cleaned_data.get('email')
        email_count = UserProfile.objects.filter(email=email).count()

        if email_count:
            raise ValidationError("该邮箱已经注册了哦")
        return email

    def _clean_confirm_password(self):
        """
        验证两次密码是否一致
        """
        password_1 = self.cleaned_data.get('password')
        password_2 = self.cleaned_data.get('password_confirm')
        if password_1 and password_2:
            if password_1 != password_2:
                raise ValidationError({"password_confirm": "两次密码不一致哦"})

    def clean(self):
        self._clean_confirm_password()


class LoginForm(forms.Form):
    """
    登录表单
    """
    email = fields.EmailField(
        required=True,
        widget=widgets.EmailInput(attrs={"class": "form-control",
                                         "placeholder": "请输入邮箱",
                                         "required": False}),
        error_messages={'required': "邮箱不能为空哦"}
    )

    password = fields.CharField(
        widget=widgets.PasswordInput(attrs={"class": "form-control",
                                            "placeholder": "请输入密码",
                                            "required": False}),
        required=True,
        min_length=6,
        max_length=20,
        error_messages={"required": "密码不能为空哦"}
    )

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        if email and password:
            user = UserProfile.objects.filter(email=email).first()
            if not user:
                raise ValidationError({"email": "用户名或密码错误哦"})

            else:
                ret = check_password(password, user.password)
                if not ret:
                    raise ValidationError({"email": "用户名或密码错误哦"})

