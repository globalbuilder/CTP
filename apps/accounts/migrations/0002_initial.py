# Generated by Django 5.1.3 on 2024-11-26 03:25

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
        ('training', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentprofile',
            name='training_entity',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='training.trainingentity', verbose_name='جهة التدريب'),
        ),
        migrations.AddField(
            model_name='studentprofile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='student_profile', to=settings.AUTH_USER_MODEL, verbose_name='المستخدم'),
        ),
        migrations.AddField(
            model_name='supervisorprofile',
            name='department',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.department', verbose_name='القسم'),
        ),
        migrations.AddField(
            model_name='supervisorprofile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='supervisor_profile', to=settings.AUTH_USER_MODEL, verbose_name='المستخدم'),
        ),
        migrations.AddField(
            model_name='trainingunitheadprofile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='head_profile', to=settings.AUTH_USER_MODEL, verbose_name='المستخدم'),
        ),
    ]
