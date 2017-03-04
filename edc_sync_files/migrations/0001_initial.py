# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-03 03:22
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.utils.timezone
import django_revision.revision_field
import edc_base.model.fields.hostname_modification_field
import edc_base.model.fields.userfield
import edc_base.model.fields.uuid_auto_field
import edc_base.utils


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='History',
            fields=[
                ('created', models.DateTimeField(blank=True, default=edc_base.utils.get_utcnow)),
                ('modified', models.DateTimeField(blank=True, default=edc_base.utils.get_utcnow)),
                ('user_created', edc_base.model.fields.userfield.UserField(blank=True, max_length=50, verbose_name='user created')),
                ('user_modified', edc_base.model.fields.userfield.UserField(blank=True, max_length=50, verbose_name='user modified')),
                ('hostname_created', models.CharField(blank=True, default='bcpp010', help_text='System field. (modified on create only)', max_length=50)),
                ('hostname_modified', edc_base.model.fields.hostname_modification_field.HostnameModificationField(blank=True, help_text='System field. (modified on every save)', max_length=50)),
                ('revision', django_revision.revision_field.RevisionField(blank=True, editable=False, help_text='System field. Git repository tag:branch:commit.', max_length=75, null=True, verbose_name='Revision')),
                ('id', edc_base.model.fields.uuid_auto_field.UUIDAutoField(blank=True, editable=False, help_text='System auto field. UUID primary key.', primary_key=True, serialize=False)),
                ('filename', models.CharField(max_length=100, unique=True)),
                ('hostname', models.CharField(max_length=100)),
                ('sent_datetime', models.DateTimeField(default=django.utils.timezone.now)),
                ('acknowledged', models.BooleanField(default=False)),
                ('approval_code', models.CharField(blank=True, max_length=50, null=True)),
                ('ack_datetime', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('ack_user', models.CharField(blank=True, max_length=50, null=True)),
            ],
            options={
                'ordering': ('-sent_datetime',),
                'verbose_name': 'Sent History',
                'verbose_name_plural': 'Sent History',
            },
        ),
        migrations.CreateModel(
            name='UploadSkipDays',
            fields=[
                ('created', models.DateTimeField(blank=True, default=edc_base.utils.get_utcnow)),
                ('modified', models.DateTimeField(blank=True, default=edc_base.utils.get_utcnow)),
                ('user_created', edc_base.model.fields.userfield.UserField(blank=True, max_length=50, verbose_name='user created')),
                ('user_modified', edc_base.model.fields.userfield.UserField(blank=True, max_length=50, verbose_name='user modified')),
                ('hostname_created', models.CharField(blank=True, default='bcpp010', help_text='System field. (modified on create only)', max_length=50)),
                ('hostname_modified', edc_base.model.fields.hostname_modification_field.HostnameModificationField(blank=True, help_text='System field. (modified on every save)', max_length=50)),
                ('revision', django_revision.revision_field.RevisionField(blank=True, editable=False, help_text='System field. Git repository tag:branch:commit.', max_length=75, null=True, verbose_name='Revision')),
                ('id', edc_base.model.fields.uuid_auto_field.UUIDAutoField(blank=True, editable=False, help_text='System auto field. UUID primary key.', primary_key=True, serialize=False)),
                ('skip_date', models.DateField(default=datetime.date(2017, 3, 3))),
                ('skip_until_date', models.DateField(blank=True, help_text='System will assume all days are skip days until this date.', null=True)),
                ('identifier', models.CharField(max_length=50)),
            ],
            options={
                'ordering': ('-created',),
            },
        ),
        migrations.CreateModel(
            name='UploadTransactionFile',
            fields=[
                ('created', models.DateTimeField(blank=True, default=edc_base.utils.get_utcnow)),
                ('modified', models.DateTimeField(blank=True, default=edc_base.utils.get_utcnow)),
                ('user_created', edc_base.model.fields.userfield.UserField(blank=True, max_length=50, verbose_name='user created')),
                ('user_modified', edc_base.model.fields.userfield.UserField(blank=True, max_length=50, verbose_name='user modified')),
                ('hostname_created', models.CharField(blank=True, default='bcpp010', help_text='System field. (modified on create only)', max_length=50)),
                ('hostname_modified', edc_base.model.fields.hostname_modification_field.HostnameModificationField(blank=True, help_text='System field. (modified on every save)', max_length=50)),
                ('revision', django_revision.revision_field.RevisionField(blank=True, editable=False, help_text='System field. Git repository tag:branch:commit.', max_length=75, null=True, verbose_name='Revision')),
                ('id', edc_base.model.fields.uuid_auto_field.UUIDAutoField(blank=True, editable=False, help_text='System auto field. UUID primary key.', primary_key=True, serialize=False)),
                ('transaction_file', models.FileField(upload_to='/Users/tsetsiba/source/bcpp/media')),
                ('file_name', models.CharField(editable=False, max_length=50, null=True, unique=True)),
                ('file_date', models.DateField(editable=False, null=True)),
                ('identifier', models.CharField(max_length=50, null=True)),
                ('consume', models.BooleanField(default=True)),
                ('total', models.IntegerField(default=0, editable=False)),
                ('consumed', models.IntegerField(default=0, editable=False)),
                ('not_consumed', models.IntegerField(default=0, editable=False, help_text='duplicates')),
                ('producer', models.TextField(editable=False, help_text='List of producers detected from the file.', max_length=1000, null=True)),
            ],
            options={
                'ordering': ('-created',),
            },
        ),
        migrations.AlterUniqueTogether(
            name='uploadskipdays',
            unique_together=set([('skip_date', 'identifier')]),
        ),
        migrations.AlterUniqueTogether(
            name='history',
            unique_together=set([('filename', 'hostname')]),
        ),
    ]
