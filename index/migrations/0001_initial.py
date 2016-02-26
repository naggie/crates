# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-26 00:06
from __future__ import unicode_literals

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
            name='Album',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('cover_art_ref', models.CharField(help_text=b'CAS ref of album/cover art', max_length=64, null=True)),
                ('artist', models.CharField(max_length=64, null=True)),
                ('colour', models.CharField(max_length=7, null=True)),
                ('mbid', models.UUIDField(blank=True, help_text=b'MusicBrainz ID', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='AudioFile',
            fields=[
                ('ref', models.CharField(help_text=b'CAS ref of file', max_length=64, primary_key=True, serialize=False)),
                ('hits', models.IntegerField(default=0, help_text=b'Number of times the file has been played/read')),
                ('size', models.IntegerField(editable=False, help_text=b'Size of file in bytes')),
                ('origin', models.CharField(blank=True, help_text=b'Where the file came from, local path or HTTP url etc', max_length=255, null=True)),
                ('added', models.DateTimeField(auto_now=True)),
                ('type', models.CharField(choices=[(b'MIX', b'Mix/Compilation'), (b'SAM', b'Sample'), (b'EP', b'Extended play'), (b'LOOP', b'Drum loop'), (b'ACCA', b'Acapella'), (b'TRAC', b'Track')], default=b'TRAC', help_text=b'Type of audio file', max_length=4, null=True)),
                ('extension', models.CharField(choices=[(b'.mp3', b'MP3: MPEG-2 Audio Layer III'), (b'.flac', b'FLAC: Free Lossless Audio Codec'), (b'.ogg', b'OGG: Ogg vorbis'), (b'.m4a', b'AAC: Apple audio codec')], help_text=b'Codec/filetype of audio file', max_length=5)),
                ('title', models.CharField(max_length=64, null=True)),
                ('artist', models.CharField(max_length=64, null=True)),
                ('album', models.CharField(max_length=64, null=True)),
                ('album_artist', models.CharField(max_length=64, null=True)),
                ('cover_art_ref', models.CharField(help_text=b'CAS ref of album/cover art', max_length=64, null=True)),
                ('colour', models.CharField(max_length=7, null=True)),
                ('composer', models.CharField(max_length=64, null=True)),
                ('genre', models.CharField(max_length=64, null=True)),
                ('year', models.PositiveSmallIntegerField(blank=True, help_text=b'Year song was released', null=True)),
                ('track', models.PositiveSmallIntegerField(blank=True, help_text=b'Track on CD release', null=True)),
                ('bitrate_kbps', models.PositiveSmallIntegerField(blank=True, help_text=b'MP3/FLAC/etc bitrate', null=True)),
                ('length', models.PositiveSmallIntegerField(blank=True, help_text=b'Approximate length in seconds', null=True)),
                ('bpm', models.PositiveSmallIntegerField(blank=True, help_text=b'Detected beats-per-minute of song', null=True)),
                ('mbid', models.UUIDField(blank=True, help_text=b'MusicBrainz ID', null=True)),
                ('album_object', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='index.Album')),
                ('deprecated_by', models.ForeignKey(help_text=b'If a mutator finds or creates a better file, it can be\n            linked here. Garbage collection can remove all files that have been\n            deprecated from the CAS, saving disk. Future crawls will not add\n            the file to the CAS any more.', null=True, on_delete=django.db.models.deletion.CASCADE, to='index.AudioFile')),
                ('user', models.ForeignKey(help_text=b'From whom the file came from', null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
