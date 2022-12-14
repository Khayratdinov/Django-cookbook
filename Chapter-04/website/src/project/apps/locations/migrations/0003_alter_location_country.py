# Generated by Django 4.1.2 on 2022-10-17 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0002_location_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='country',
            field=models.CharField(blank=True, choices=[('BE', 'Belgium'), ('BG', 'Bulgaria'), ('CZ', 'Czechia'), ('DK', 'Denmark'), ('DE', 'Germany'), ('EE', 'Estonia'), ('IE', 'Ireland'), ('EL', 'Greece'), ('ES', 'Spain'), ('FR', 'France'), ('HR', 'Croatia'), ('IT', 'Italy'), ('CY', 'Cyprus'), ('LV', 'Latvia'), ('LT', 'Lithuania'), ('LU', 'Luxembourg'), ('HU', 'Hungary'), ('MT', 'Malta'), ('NL', 'Netherlands'), ('AT', 'Austria'), ('PL', 'Poland'), ('PT', 'Portugal'), ('RO', 'Romania'), ('SI', 'Slovenia'), ('SK', 'Slovakia'), ('FI', 'Finland'), ('SE', 'Sweden'), ('UK', 'United Kingdom')], max_length=255, verbose_name='Country'),
        ),
    ]
