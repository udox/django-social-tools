# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'BannedUser'
        db.create_table(u'social_banneduser', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('handle', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('reason', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'social', ['BannedUser'])

        # Adding model 'SearchTerm'
        db.create_table(u'social_searchterm', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('term', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'social', ['SearchTerm'])

        # Adding model 'SocialPost'
        db.create_table(u'social_socialpost', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')()),
            ('uid', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('post_url', self.gf('django.db.models.fields.URLField')(max_length=255, null=True, blank=True)),
            ('handle', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('followers', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('user_joined', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('profile_image', self.gf('django.db.models.fields.URLField')(max_length=255, null=True, blank=True)),
            ('content', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('approved', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('high_priority', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('entry_allowed', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('notes', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('account', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['brand.MarketAccount'], null=True, blank=True)),
            ('image_url', self.gf('django.db.models.fields.URLField')(max_length=255, null=True, blank=True)),
            ('messaged', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('sent_message', self.gf('django.db.models.fields.CharField')(max_length=140, null=True, blank=True)),
            ('messaged_by', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='socialpost_messenger', null=True, to=orm['auth.User'])),
            ('messaged_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('sent_id', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('disallowed_reason', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('raw_object', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'social', ['SocialPost'])


    def backwards(self, orm):
        # Deleting model 'BannedUser'
        db.delete_table(u'social_banneduser')

        # Deleting model 'SearchTerm'
        db.delete_table(u'social_searchterm')

        # Deleting model 'SocialPost'
        db.delete_table(u'social_socialpost')


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
        u'brand.marketaccount': {
            'Meta': {'object_name': 'MarketAccount'},
            'access_token_key': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'access_token_secret': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'client_id': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'client_secret': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'consumer_key': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'consumer_secret': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'handle': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'social.banneduser': {
            'Meta': {'object_name': 'BannedUser'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'handle': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'reason': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        u'social.searchterm': {
            'Meta': {'object_name': 'SearchTerm'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'term': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'social.socialpost': {
            'Meta': {'ordering': "('-high_priority', '-created_at', '-followers', 'handle')", 'object_name': 'SocialPost'},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['brand.MarketAccount']", 'null': 'True', 'blank': 'True'}),
            'approved': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'content': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'disallowed_reason': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'entry_allowed': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'followers': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'handle': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'high_priority': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_url': ('django.db.models.fields.URLField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'messaged': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'messaged_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'messaged_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'socialpost_messenger'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'post_url': ('django.db.models.fields.URLField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'profile_image': ('django.db.models.fields.URLField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'raw_object': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'sent_id': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'sent_message': ('django.db.models.fields.CharField', [], {'max_length': '140', 'null': 'True', 'blank': 'True'}),
            'uid': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'user_joined': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['social']