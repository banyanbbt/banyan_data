# Generated by Django 2.0.7 on 2018-07-31 06:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0003_task_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='question_received',
            field=models.IntegerField(default=0, verbose_name='已被领取的题目数量'),
        ),
    ]
