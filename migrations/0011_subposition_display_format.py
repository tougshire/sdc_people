# Generated by Django 5.0.3 on 2024-04-23 11:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sdc_people', '0010_alter_personnote_expiration'),
    ]

    operations = [
        migrations.AddField(
            model_name='subposition',
            name='display_format',
            field=models.CharField(default='{position} {committee}', help_text='The format to display the subposition name and commmittee name in a list. Should include "\\{position\\}", "\\{committee\\}", or both', max_length=60),
        ),
    ]