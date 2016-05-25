# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-30 05:39
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('django_blog_it', '0004_posthistory'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserRole',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(choices=[('Drafted', 'Drafted'), ('Published', 'Published'), ('Rejected', 'Rejected'), ('Trashed', 'Trashed')], max_length=10)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterField(
            model_name='image_file',
            name='thumbnail',
            field=models.FileField(blank=True, null=True, upload_to='static/uploads/%Y/%m/%d/'),
        ),
        migrations.AlterField(
            model_name='image_file',
            name='upload',
            field=models.FileField(upload_to='static/uploads/%Y/%m/%d/'),
        ),
        migrations.AlterField(
            model_name='post',
            name='status',
            field=models.CharField(choices=[('Drafted', 'Drafted'), ('Published', 'Published'), ('Rejected', 'Rejected'), ('Trashed', 'Trashed')], default='Drafted', max_length=10),
        ),
    ]