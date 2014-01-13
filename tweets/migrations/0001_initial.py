# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'MarketAccount'
        db.create_table(u'tweets_marketaccount', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('handle', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('consumer_secret', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('consumer_key', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('access_token_secret', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('access_token_key', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'tweets', ['MarketAccount'])

        # Adding model 'Message'
        db.create_table(u'tweets_message', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('copy', self.gf('django.db.models.fields.CharField')(max_length=140)),
            ('account', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tweets.MarketAccount'])),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=1)),
        ))
        db.send_create_signal(u'tweets', ['Message'])

        # Adding model 'Tweet'
        db.create_table(u'tweets_tweet', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')()),
            ('uid', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('handle', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('followers', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('content', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('image_url', self.gf('django.db.models.fields.URLField')(max_length=255, null=True, blank=True)),
            ('tweeted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('approved', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('photoshop', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('notes', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('account', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tweets.MarketAccount'], null=True, blank=True)),
            ('sent_tweet', self.gf('django.db.models.fields.CharField')(max_length=140, null=True, blank=True)),
            ('artworker', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='artworker', null=True, to=orm['auth.User'])),
            ('tweeted_by', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='tweeter', null=True, to=orm['auth.User'])),
            ('tweeted_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('tweet_id', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal(u'tweets', ['Tweet'])

        # Adding model 'SearchTerm'
        db.create_table(u'tweets_searchterm', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('term', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'tweets', ['SearchTerm'])


    def backwards(self, orm):
        # Deleting model 'MarketAccount'
        db.delete_table(u'tweets_marketaccount')

        # Deleting model 'Message'
        db.delete_table(u'tweets_message')

        # Deleting model 'Tweet'
        db.delete_table(u'tweets_tweet')

        # Deleting model 'SearchTerm'
        db.delete_table(u'tweets_searchterm')


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
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'tweets.marketaccount': {
            'Meta': {'object_name': 'MarketAccount'},
            'access_token_key': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'access_token_secret': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'consumer_key': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'consumer_secret': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'handle': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'tweets.message': {
            'Meta': {'object_name': 'Message'},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tweets.MarketAccount']"}),
            'copy': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '1'})
        },
        u'tweets.searchterm': {
            'Meta': {'object_name': 'SearchTerm'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'term': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'tweets.tweet': {
            'Meta': {'ordering': "('-created_at', '-followers', 'handle')", 'object_name': 'Tweet'},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tweets.MarketAccount']", 'null': 'True', 'blank': 'True'}),
            'approved': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'artworker': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'artworker'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'content': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'followers': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'handle': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_url': ('django.db.models.fields.URLField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'photoshop': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'sent_tweet': ('django.db.models.fields.CharField', [], {'max_length': '140', 'null': 'True', 'blank': 'True'}),
            'tweet_id': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'tweeted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'tweeted_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'tweeted_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'tweeter'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'uid': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        }
    }

    complete_apps = ['tweets']