# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'MarketAccount'
        db.create_table(u'brand_marketaccount', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('type', self.gf('django.db.models.fields.CharField')(unique=True, max_length=1)),
            ('handle', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('client_id', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('client_secret', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('consumer_secret', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('consumer_key', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('access_token_secret', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('access_token_key', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal(u'brand', ['MarketAccount'])

        # Adding model 'Message'
        db.create_table(u'brand_message', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('copy', self.gf('django.db.models.fields.CharField')(max_length=140)),
            ('account', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['brand.MarketAccount'])),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=1)),
        ))
        db.send_create_signal(u'brand', ['Message'])


    def backwards(self, orm):
        # Deleting model 'MarketAccount'
        db.delete_table(u'brand_marketaccount')

        # Deleting model 'Message'
        db.delete_table(u'brand_message')


    models = {
        u'brand.marketaccount': {
            'Meta': {'object_name': 'MarketAccount'},
            'access_token_key': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'access_token_secret': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'client_id': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'client_secret': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'consumer_key': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'consumer_secret': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'handle': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '1'})
        },
        u'brand.message': {
            'Meta': {'object_name': 'Message'},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['brand.MarketAccount']"}),
            'copy': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '1'})
        }
    }

    complete_apps = ['brand']