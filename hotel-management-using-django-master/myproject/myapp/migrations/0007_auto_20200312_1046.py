# Generated by Django 2.1.5 on 2020-03-12 04:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0006_auto_20200312_1045'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='staff',
            name='height_field',
        ),
        migrations.RemoveField(
            model_name='staff',
            name='width_field',
        ),
        migrations.AlterField(
            model_name='staff',
            name='profile_picture',
            field=models.ImageField(default='image/staff.png', upload_to='staff_img', verbose_name='Own Picture'),
        ),
    ]