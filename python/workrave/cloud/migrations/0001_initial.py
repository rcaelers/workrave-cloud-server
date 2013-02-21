# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Client'
        db.create_table(u'cloud_client', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', unique=True, blank=True, to=orm['auth.User'])),
            ('last_seen', self.gf('django.db.models.fields.DateTimeField')()),
            ('uuid', self.gf('django.db.models.fields.CharField')(unique=True, max_length=32)),
        ))
        db.send_create_signal(u'cloud', ['Client'])

        # Adding model 'State'
        db.create_table(u'cloud_state', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(related_name='state', unique=True, blank=True, to=orm['auth.User'])),
            ('time', self.gf('django.db.models.fields.DateTimeField')()),
            ('timezone', self.gf('django.db.models.fields.IntegerField')()),
            ('active', self.gf('django.db.models.fields.CharField')(max_length=36)),
            ('state', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'cloud', ['State'])

        # Adding model 'Configuration'
        db.create_table(u'cloud_configuration', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(related_name='configuration', unique=True, blank=True, to=orm['auth.User'])),
            ('configuration', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'cloud', ['Configuration'])

        # Adding model 'Statistics'
        db.create_table(u'cloud_statistics', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(related_name='statistics', to=orm['auth.User'])),
            ('date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('start_time', self.gf('django.db.models.fields.DateTimeField')()),
            ('stop_time', self.gf('django.db.models.fields.DateTimeField')()),
            ('total_active_time', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('total_click_movement', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('total_mouse_movement', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('total_movement_time', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('total_clicks', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('total_keystrokes', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('micro_break', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['cloud.BreakStatistics'])),
            ('rest_break', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['cloud.BreakStatistics'])),
            ('daily_limit', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['cloud.BreakStatistics'])),
        ))
        db.send_create_signal(u'cloud', ['Statistics'])

        # Adding model 'BreakStatistics'
        db.create_table(u'cloud_breakstatistics', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('prompted', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('taken', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('natural_taken', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('skipped', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('postponed', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('unique', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('total_overdue', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'cloud', ['BreakStatistics'])


    def backwards(self, orm):
        # Deleting model 'Client'
        db.delete_table(u'cloud_client')

        # Deleting model 'State'
        db.delete_table(u'cloud_state')

        # Deleting model 'Configuration'
        db.delete_table(u'cloud_configuration')

        # Deleting model 'Statistics'
        db.delete_table(u'cloud_statistics')

        # Deleting model 'BreakStatistics'
        db.delete_table(u'cloud_breakstatistics')


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
        u'cloud.breakstatistics': {
            'Meta': {'object_name': 'BreakStatistics'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'natural_taken': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'postponed': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'prompted': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'skipped': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'taken': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'total_overdue': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'unique': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'cloud.client': {
            'Meta': {'object_name': 'Client'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_seen': ('django.db.models.fields.DateTimeField', [], {}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'unique': 'True', 'blank': 'True', 'to': u"orm['auth.User']"}),
            'uuid': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '32'})
        },
        u'cloud.configuration': {
            'Meta': {'ordering': "('created',)", 'object_name': 'Configuration'},
            'configuration': ('django.db.models.fields.TextField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'configuration'", 'unique': 'True', 'blank': 'True', 'to': u"orm['auth.User']"})
        },
        u'cloud.state': {
            'Meta': {'ordering': "('created',)", 'object_name': 'State'},
            'active': ('django.db.models.fields.CharField', [], {'max_length': '36'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'state'", 'unique': 'True', 'blank': 'True', 'to': u"orm['auth.User']"}),
            'state': ('django.db.models.fields.TextField', [], {}),
            'time': ('django.db.models.fields.DateTimeField', [], {}),
            'timezone': ('django.db.models.fields.IntegerField', [], {})
        },
        u'cloud.statistics': {
            'Meta': {'ordering': "('created',)", 'object_name': 'Statistics'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'daily_limit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': u"orm['cloud.BreakStatistics']"}),
            'date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'micro_break': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': u"orm['cloud.BreakStatistics']"}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'statistics'", 'to': u"orm['auth.User']"}),
            'rest_break': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': u"orm['cloud.BreakStatistics']"}),
            'start_time': ('django.db.models.fields.DateTimeField', [], {}),
            'stop_time': ('django.db.models.fields.DateTimeField', [], {}),
            'total_active_time': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'total_click_movement': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'total_clicks': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'total_keystrokes': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'total_mouse_movement': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'total_movement_time': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['cloud']