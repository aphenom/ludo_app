# Generated by Django 4.2.16 on 2024-10-13 01:58

from django.db import migrations
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('player', '0008_alter_visiteur_visiteur_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profil',
            name='pays_residence',
            field=django_countries.fields.CountryField(blank=True, max_length=2, null=True, verbose_name='pays'),
        ),
    ]
