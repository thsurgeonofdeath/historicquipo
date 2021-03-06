# Generated by Django 4.0.3 on 2022-03-22 08:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('monument', '0005_alter_monument_latitude_alter_monument_longitude'),
    ]

    operations = [
        migrations.CreateModel(
            name='SavedMonument',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('monument', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='monument.monument')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
