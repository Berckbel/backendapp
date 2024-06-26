# Generated by Django 5.0.6 on 2024-05-12 00:15

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('external_id', models.CharField(max_length=60, unique=True)),
                ('score', models.DecimalField(decimal_places=2, max_digits=12)),
                ('status', models.IntegerField(choices=[(1, 'Active'), (2, 'Inactive')], default=1)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('preapproved_at', models.DateTimeField(blank=True, null=True)),
            ],
        ),
    ]
