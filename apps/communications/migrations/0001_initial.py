# Generated by Django 5.1.3 on 2024-11-26 03:25

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=200, verbose_name='الموضوع')),
                ('body', models.TextField(verbose_name='المحتوى')),
                ('sent_date', models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الإرسال')),
                ('read', models.BooleanField(default=False, verbose_name='تم القراءة')),
                ('attachment', models.FileField(blank=True, null=True, upload_to='messages/', verbose_name='مرفق')),
                ('recipient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='received_messages', to=settings.AUTH_USER_MODEL, verbose_name='المستقبل')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sent_messages', to=settings.AUTH_USER_MODEL, verbose_name='المرسل')),
            ],
        ),
    ]