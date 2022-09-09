# MEPP - A web application to guide patients and clinicians in the process of
# facial palsy rehabilitation, with the help of the mirror effect and principles
# of motor learning
# Copyright (C) 2021 MEPP <info@mirroreffectplus.org>
#
# This file is part of MEPP.
#
# MEPP is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# MEPP is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with MEPP.  If not, see <http://www.gnu.org/licenses/>.

# Generated by Django 3.2.9 on 2022-09-09 18:54

from django.db import migrations, models
import django.utils.timezone
import mepp.api.models.expiring_token


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20211104_1807'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='expiringtoken',
            options={'ordering': ['-created_date'], 'verbose_name': 'Token', 'verbose_name_plural': 'Tokens'},
        ),
        migrations.AddField(
            model_name='expiringtoken',
            name='created_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='expiringtoken',
            name='expiry_date',
            field=models.DateTimeField(default=mepp.api.models.expiring_token.get_expiry_date),
        ),
    ]