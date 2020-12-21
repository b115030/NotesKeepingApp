# Generated by Django 3.1.3 on 2020-12-21 04:51

import colorfield.fields
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
            name='Note',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default=None, max_length=150)),
                ('description', models.TextField()),
                ('created_time', models.DateTimeField(auto_now_add=True, null=True)),
                ('is_archived', models.BooleanField(default=False)),
                ('is_deleted', models.BooleanField(default=False)),
                ('color', colorfield.fields.ColorField(default='#00F0FF', max_length=18)),
                ('image', models.ImageField(default=None, null=True, upload_to='note_images/')),
                ('trash', models.BooleanField(default=False)),
                ('is_pinned', models.BooleanField(default=False)),
                ('archive_time', models.DateTimeField(blank=True, null=True)),
                ('trash_time', models.DateTimeField(blank=True, null=True)),
                ('reminder_date', models.DateTimeField(blank=True, null=True)),
                ('collaborate', models.ManyToManyField(blank=True, null=True, related_name='collaborated_user', to=settings.AUTH_USER_MODEL)),
                ('label', models.ManyToManyField(blank=True, related_name='label', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='owner', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
