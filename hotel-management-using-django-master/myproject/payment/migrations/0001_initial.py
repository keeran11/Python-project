# Generated by Django 2.0 on 2020-03-04 05:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('myapp', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CheckIn',
            fields=[
                ('id', models.CharField(blank=True, max_length=50, primary_key=True, serialize=False)),
                ('rooms', models.CharField(blank=True, editable=False, max_length=50, verbose_name='Room number')),
                ('initial_amount', models.PositiveIntegerField(blank=True, editable=False, verbose_name='Initial Price')),
                ('check_in_date_time', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('last_edited_on', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('reservation', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='myapp.Reservation', verbose_name='Reservation')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='User name')),
            ],
            options={
                'verbose_name': 'CheckIn',
                'verbose_name_plural': 'CheckIn Information',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Checkout',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stay_duration', models.DurationField(editable=False, null=True)),
                ('total_amount', models.PositiveIntegerField(default=0, editable=False)),
                ('pay_amount', models.PositiveIntegerField(default=0, editable=False)),
                ('check_out_date_time', models.DateTimeField(editable=False, null=True)),
                ('check_in', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='payment.CheckIn')),
                ('user', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Checkout',
                'verbose_name_plural': 'CheckOut Information',
                'ordering': ['-check_in'],
            },
        ),
    ]