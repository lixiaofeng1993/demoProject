# Generated by Django 3.2.16 on 2024-02-27 12:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nb', '0006_message'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='date',
            field=models.DateTimeField(help_text='写入时间(天)', null=True, verbose_name='写入时间'),
        ),
    ]
