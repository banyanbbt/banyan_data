# Generated by Django 2.0.7 on 2018-07-31 07:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0006_remove_task_question_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='attachment_id',
            field=models.IntegerField(blank=True, db_index=True, null=True, verbose_name='附件id'),
        ),
    ]