# Generated by Django 3.2 on 2022-11-08 17:21

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tests_representation', '0004_change_testplan_parent_related_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='testresult',
            name='execution_time',
            field=models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0)]),
        ),
    ]
