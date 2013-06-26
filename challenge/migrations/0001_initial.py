# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Challenge_User'
        db.create_table(u'challenge_challenge_user', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('bio', self.gf('django.db.models.fields.TextField')(default='please add some content here')),
            ('added_username', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'challenge', ['Challenge_User'])

        # Adding model 'Category'
        db.create_table(u'challenge_category', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
        ))
        db.send_create_signal(u'challenge', ['Category'])

        # Adding model 'Challenge'
        db.create_table(u'challenge_challenge', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('title', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('slug', self.gf('autoslug.fields.AutoSlugField')(unique=True, max_length=50, populate_from='title', unique_with=())),
            ('content', self.gf('django.db.models.fields.TextField')(default='please add some content here')),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['challenge.Category'])),
            ('status', self.gf('django.db.models.fields.CharField')(default='Uncomplete', max_length=32)),
            ('date_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'challenge', ['Challenge'])

        # Adding model 'Claim'
        db.create_table(u'challenge_claim', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('challenge', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['challenge.Challenge'])),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('content', self.gf('django.db.models.fields.TextField')(default='please add some content here')),
            ('project_url', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('proof_url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('status', self.gf('django.db.models.fields.CharField')(default='Pending', max_length=32)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'challenge', ['Claim'])

        # Adding unique constraint on 'Claim', fields ['challenge', 'author']
        db.create_unique(u'challenge_claim', ['challenge_id', 'author_id'])

        # Adding model 'Vote'
        db.create_table(u'challenge_vote', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('challenge', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['challenge.Challenge'])),
            ('direction', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'challenge', ['Vote'])

        # Adding unique constraint on 'Vote', fields ['challenge', 'user']
        db.create_unique(u'challenge_vote', ['challenge_id', 'user_id'])

        # Adding model 'Award'
        db.create_table(u'challenge_award', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('about', self.gf('django.db.models.fields.TextField')(default='please add some content here')),
            ('icon', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'challenge', ['Award'])


    def backwards(self, orm):
        # Removing unique constraint on 'Vote', fields ['challenge', 'user']
        db.delete_unique(u'challenge_vote', ['challenge_id', 'user_id'])

        # Removing unique constraint on 'Claim', fields ['challenge', 'author']
        db.delete_unique(u'challenge_claim', ['challenge_id', 'author_id'])

        # Deleting model 'Challenge_User'
        db.delete_table(u'challenge_challenge_user')

        # Deleting model 'Category'
        db.delete_table(u'challenge_category')

        # Deleting model 'Challenge'
        db.delete_table(u'challenge_challenge')

        # Deleting model 'Claim'
        db.delete_table(u'challenge_claim')

        # Deleting model 'Vote'
        db.delete_table(u'challenge_vote')

        # Deleting model 'Award'
        db.delete_table(u'challenge_award')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'challenge.award': {
            'Meta': {'object_name': 'Award'},
            'about': ('django.db.models.fields.TextField', [], {'default': "'please add some content here'"}),
            'icon': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        u'challenge.category': {
            'Meta': {'object_name': 'Category'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        u'challenge.challenge': {
            'Meta': {'object_name': 'Challenge'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['challenge.Category']"}),
            'content': ('django.db.models.fields.TextField', [], {'default': "'please add some content here'"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique': 'True', 'max_length': '50', 'populate_from': "'title'", 'unique_with': '()'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'Uncomplete'", 'max_length': '32'}),
            'title': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        u'challenge.challenge_user': {
            'Meta': {'object_name': 'Challenge_User'},
            'added_username': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'bio': ('django.db.models.fields.TextField', [], {'default': "'please add some content here'"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'})
        },
        u'challenge.claim': {
            'Meta': {'unique_together': "(('challenge', 'author'),)", 'object_name': 'Claim'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'challenge': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['challenge.Challenge']"}),
            'content': ('django.db.models.fields.TextField', [], {'default': "'please add some content here'"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'project_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'proof_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'Pending'", 'max_length': '32'})
        },
        u'challenge.vote': {
            'Meta': {'unique_together': "(('challenge', 'user'),)", 'object_name': 'Vote'},
            'challenge': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['challenge.Challenge']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'direction': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['challenge']