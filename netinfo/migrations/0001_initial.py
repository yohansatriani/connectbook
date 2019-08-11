# Generated by Django 2.2.3 on 2019-08-11 16:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='sites',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100, unique=True)),
                ('alias_name', models.CharField(max_length=100, unique=True)),
                ('type', models.CharField(max_length=50)),
                ('location', models.CharField(default='', max_length=300, null=True)),
                ('city', models.CharField(default='', max_length=100, null=True)),
                ('description', models.CharField(default='', max_length=1000, null=True)),
                ('ip_address', models.CharField(default='0.0.0.0/0', max_length=100, null=True)),
                ('tagline', models.CharField(default='', max_length=500, null=True)),
                ('add_field1', models.CharField(max_length=100, null=True)),
                ('add_field2', models.CharField(max_length=100, null=True)),
                ('add_field3', models.CharField(max_length=100, null=True)),
                ('add_field4', models.CharField(max_length=100, null=True)),
            ],
            options={
                'verbose_name_plural': 'sites',
            },
        ),
        migrations.CreateModel(
            name='contacts',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('type', models.CharField(default='', max_length=10)),
                ('contact_number', models.CharField(default='', max_length=50)),
                ('site', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='netinfo.sites')),
            ],
            options={
                'verbose_name_plural': 'contacts',
            },
        ),
    ]
