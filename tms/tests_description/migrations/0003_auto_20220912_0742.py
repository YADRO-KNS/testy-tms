# Generated by Django 3.2 on 2022-09-12 07:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tests_description', '0002_testcase'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='testcase',
            options={'default_related_name': 'test_cases'},
        ),
        migrations.AlterModelOptions(
            name='testsuite',
            options={'default_related_name': 'test_suites'},
        ),
    ]