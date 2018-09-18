# Generated by Django 2.0.7 on 2018-08-03 10:20

from django.db import migrations, models
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('question', '0010_auto_20180802_2023'),
    ]

    operations = [
        migrations.CreateModel(
            name='KnownAnswer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('question_id', models.IntegerField(blank=True, db_index=True, null=True, verbose_name='已知答案id')),
                ('content', jsonfield.fields.JSONField(blank=True, null=True, verbose_name='已知答案')),
            ],
            options={
                'verbose_name_plural': '已知答案',
                'db_table': 'known_answer',
                'verbose_name': '已知答案',
            },
        ),
        migrations.AddField(
            model_name='question',
            name='has_known_answer',
            field=models.BooleanField(default=False, verbose_name='有已知答案'),
        ),
        migrations.AddField(
            model_name='question',
            name='name',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='题目名称'),
        ),
        migrations.AlterField(
            model_name='answeroption',
            name='is_required',
            field=models.BooleanField(default=True, verbose_name='输入项是否必填'),
        ),
    ]