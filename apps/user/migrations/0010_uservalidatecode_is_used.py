# Generated by Django 2.0.7 on 2018-08-07 09:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0009_userwithdraw_wallet_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='uservalidatecode',
            name='is_used',
            field=models.BooleanField(default=False, verbose_name='验证码是否被使用'),
        ),
    ]
