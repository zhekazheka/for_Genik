# Generated by Django 2.2.3 on 2019-07-16 21:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('my_test', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cvsmodel',
            old_name='alpha_a',
            new_name='value',
        ),
        migrations.RemoveField(
            model_name='cvsmodel',
            name='alpha_b',
        ),
    ]
