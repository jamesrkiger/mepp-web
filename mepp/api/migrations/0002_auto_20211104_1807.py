# Generated by Django 3.2.9 on 2021-11-04 18:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expiringtoken',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='auth_token', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddConstraint(
            model_name='expiringtoken',
            constraint=models.UniqueConstraint(fields=('key', 'user', 'temporary'), name='token_unique'),
        ),
    ]