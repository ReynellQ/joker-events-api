# Generated by Django 4.0.5 on 2022-06-24 18:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Events',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('lugar', models.CharField(max_length=100)),
                ('aforo', models.IntegerField()),
                ('description', models.TextField()),
                ('precioBoleta', models.DecimalField(decimal_places=2, default=0.0, max_digits=14)),
                ('image', models.CharField(blank=True, max_length=200)),
                ('fechaInicio', models.DateField()),
                ('fechaFin', models.DateField()),
                ('gmaps', models.CharField(max_length=100)),
                ('disponible', models.IntegerField()),
                ('contacto', models.CharField(default='', max_length=100)),
                ('createdAt', models.DateField()),
                ('visible', models.BooleanField(default=True)),
                ('createdBy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'events',
                'order_with_respect_to': 'fechaInicio',
            },
        ),
        migrations.CreateModel(
            name='MediaEvents',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('element', models.IntegerField()),
                ('media', models.CharField(max_length=200)),
                ('id_event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events.events')),
            ],
            options={
                'db_table': 'media_events',
            },
        ),
    ]
