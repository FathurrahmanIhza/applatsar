# Generated by Django 4.1.1 on 2022-09-30 17:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Stasiun',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama', models.CharField(max_length=20)),
                ('lokasi', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Databasegempa',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tanggal', models.DateField(null=True)),
                ('jam', models.TimeField(null=True)),
                ('lintang', models.DecimalField(decimal_places=2, max_digits=4, null=True)),
                ('bujur', models.DecimalField(decimal_places=2, max_digits=4, null=True)),
                ('kedalaman', models.IntegerField(null=True)),
                ('magnitudo', models.DecimalField(decimal_places=2, max_digits=4, null=True)),
                ('keterangan', models.CharField(max_length=50, null=True)),
                ('stasiun_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='applatsar.stasiun')),
            ],
        ),
    ]
