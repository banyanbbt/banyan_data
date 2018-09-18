# Generated by Django 2.0.7 on 2018-08-27 07:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('question', '0012_question_code'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='attachment_id',
        ),
        migrations.AddField(
            model_name='attachment',
            name='detail_id',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='附件归属表ID'),
        ),
        migrations.AddField(
            model_name='attachment',
            name='detail_type',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='附件归属表类型'),
        ),
    ]