# Generated by Django 2.0.7 on 2018-07-31 07:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('question', '0006_auto_20180731_1522'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attachment',
            name='file_obj',
            field=models.FileField(blank=True, null=True, upload_to='downloads', verbose_name='文件结果'),
        ),
    ]