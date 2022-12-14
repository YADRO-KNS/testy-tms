# Generated by Django 3.2 on 2022-10-10 09:32

from django.conf import settings
import django.contrib.postgres.fields
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('tests_description', '0001_initial'),
        ('core', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
                ('is_archive', models.BooleanField(default=False)),
                ('case', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tests', to='tests_description.testcase')),
            ],
            options={
                'default_related_name': 'tests',
            },
        ),
        migrations.CreateModel(
            name='TestResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
                ('status', models.IntegerField(choices=[(0, 'Failed'), (1, 'Passed'), (2, 'Skipped'), (3, 'Broken'), (4, 'Blocked'), (5, 'Untested')], default=5)),
                ('comment', models.TextField(blank=True)),
                ('is_archive', models.BooleanField(default=False)),
                ('test_case_version', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0)])),
                ('test', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='test_results', to='tests_representation.test')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='test_results', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'default_related_name': 'test_results',
            },
        ),
        migrations.CreateModel(
            name='TestPlan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
                ('name', models.CharField(max_length=255)),
                ('parameters', django.contrib.postgres.fields.ArrayField(base_field=models.PositiveIntegerField(blank=True, null=True), blank=True, null=True, size=None)),
                ('started_at', models.DateTimeField()),
                ('due_date', models.DateTimeField()),
                ('finished_at', models.DateTimeField(blank=True, null=True)),
                ('is_archive', models.BooleanField(default=False)),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='child_test_planes', to='tests_representation.testplan')),
            ],
            options={
                'default_related_name': 'test_plans',
            },
        ),
        migrations.AddField(
            model_name='test',
            name='plan',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tests', to='tests_representation.testplan'),
        ),
        migrations.AddField(
            model_name='test',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tests', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Parameter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
                ('data', models.TextField()),
                ('group_name', models.CharField(max_length=255)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='parameters', to='core.project')),
            ],
            options={
                'default_related_name': 'parameters',
                'unique_together': {('group_name', 'data')},
            },
        ),
    ]
