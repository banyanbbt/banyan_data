# Generated by Django 2.0.7 on 2018-08-02 08:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('question', '0007_auto_20180731_1529'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='question_type',
            field=models.CharField(blank=True, choices=[('文件翻译', '文件翻译'), ('数据清洗', '数据清洗')], max_length=255, null=True, verbose_name='题目类型'),
        ),
    ]
