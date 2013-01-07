# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Scope'
        db.create_table('oauth2_scope', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('title', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['oauth2.Scope'], null=True, blank=True)),
        ))
        db.send_create_signal('oauth2', ['Scope'])

        # Adding model 'Client'
        db.create_table('oauth2_client', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('website', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('profile', self.gf('django.db.models.fields.IntegerField')(default=2)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, blank=True)),
            ('create_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('client_id', self.gf('django.db.models.fields.CharField')(default='3a419a98820c7f324afc69e66ecc76b8', max_length=32)),
            ('client_secret', self.gf('django.db.models.fields.CharField')(default='f059afe82b92b4dd6fd28db1f0077fce', max_length=32)),
            ('redirect_uri', self.gf('django.db.models.fields.URLField')(max_length=200)),
        ))
        db.send_create_signal('oauth2', ['Client'])

        # Adding M2M table for field scopes on 'Client'
        db.create_table('oauth2_client_scopes', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('client', models.ForeignKey(orm['oauth2.client'], null=False)),
            ('scope', models.ForeignKey(orm['oauth2.scope'], null=False))
        ))
        db.create_unique('oauth2_client_scopes', ['client_id', 'scope_id'])

        # Adding model 'CodeGrant'
        db.create_table('oauth2_codegrant', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('client', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['oauth2.Client'])),
            ('code', self.gf('django.db.models.fields.CharField')(default='ae68a68a86e46a0f98141a48a66b1b7a', unique=True, max_length=32, db_index=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('tagline', self.gf('django.db.models.fields.CharField')(max_length=250, blank=True)),
            ('redirect_uri', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('create_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('expires', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2012, 12, 17, 0, 0))),
        ))
        db.send_create_signal('oauth2', ['CodeGrant'])

        # Adding M2M table for field scopes on 'CodeGrant'
        db.create_table('oauth2_codegrant_scopes', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('codegrant', models.ForeignKey(orm['oauth2.codegrant'], null=False)),
            ('scope', models.ForeignKey(orm['oauth2.scope'], null=False))
        ))
        db.create_unique('oauth2_codegrant_scopes', ['codegrant_id', 'scope_id'])

        # Adding model 'Token'
        db.create_table('oauth2_token', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('client', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['oauth2.Client'])),
            ('code', self.gf('django.db.models.fields.CharField')(default='e35d5463ba6b72d4c4d42ca00ba6a4bb', unique=True, max_length=32, db_index=True)),
            ('access_token', self.gf('django.db.models.fields.CharField')(default='145a4dcc2535ca590adf5a2204c3325f', unique=True, max_length=32, db_index=True)),
            ('refresh_token', self.gf('django.db.models.fields.CharField')(null=True, default='56832b4f342ce6119c0f6d8ddd7e17d9', max_length=32, blank=True, unique=True, db_index=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('tagline', self.gf('django.db.models.fields.CharField')(max_length=250, blank=True)),
            ('create_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('expires', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2012, 12, 17, 0, 0))),
        ))
        db.send_create_signal('oauth2', ['Token'])

        # Adding M2M table for field scopes on 'Token'
        db.create_table('oauth2_token_scopes', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('token', models.ForeignKey(orm['oauth2.token'], null=False)),
            ('scope', models.ForeignKey(orm['oauth2.scope'], null=False))
        ))
        db.create_unique('oauth2_token_scopes', ['token_id', 'scope_id'])


    def backwards(self, orm):
        # Deleting model 'Scope'
        db.delete_table('oauth2_scope')

        # Deleting model 'Client'
        db.delete_table('oauth2_client')

        # Removing M2M table for field scopes on 'Client'
        db.delete_table('oauth2_client_scopes')

        # Deleting model 'CodeGrant'
        db.delete_table('oauth2_codegrant')

        # Removing M2M table for field scopes on 'CodeGrant'
        db.delete_table('oauth2_codegrant_scopes')

        # Deleting model 'Token'
        db.delete_table('oauth2_token')

        # Removing M2M table for field scopes on 'Token'
        db.delete_table('oauth2_token_scopes')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'oauth2.client': {
            'Meta': {'object_name': 'Client'},
            'client_id': ('django.db.models.fields.CharField', [], {'default': "'3a419a98820c7f324afc69e66ecc76b8'", 'max_length': '32'}),
            'client_secret': ('django.db.models.fields.CharField', [], {'default': "'f059afe82b92b4dd6fd28db1f0077fce'", 'max_length': '32'}),
            'create_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'profile': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'redirect_uri': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'scopes': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['oauth2.Scope']", 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'oauth2.codegrant': {
            'Meta': {'object_name': 'CodeGrant'},
            'client': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['oauth2.Client']"}),
            'code': ('django.db.models.fields.CharField', [], {'default': "'ae68a68a86e46a0f98141a48a66b1b7a'", 'unique': 'True', 'max_length': '32', 'db_index': 'True'}),
            'create_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'expires': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 12, 17, 0, 0)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'redirect_uri': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'scopes': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['oauth2.Scope']", 'null': 'True', 'blank': 'True'}),
            'tagline': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'oauth2.scope': {
            'Meta': {'ordering': "['name']", 'object_name': 'Scope'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['oauth2.Scope']", 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        'oauth2.token': {
            'Meta': {'object_name': 'Token'},
            'access_token': ('django.db.models.fields.CharField', [], {'default': "'145a4dcc2535ca590adf5a2204c3325f'", 'unique': 'True', 'max_length': '32', 'db_index': 'True'}),
            'client': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['oauth2.Client']"}),
            'code': ('django.db.models.fields.CharField', [], {'default': "'e35d5463ba6b72d4c4d42ca00ba6a4bb'", 'unique': 'True', 'max_length': '32', 'db_index': 'True'}),
            'create_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'expires': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 12, 17, 0, 0)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'refresh_token': ('django.db.models.fields.CharField', [], {'null': 'True', 'default': "'56832b4f342ce6119c0f6d8ddd7e17d9'", 'max_length': '32', 'blank': 'True', 'unique': 'True', 'db_index': 'True'}),
            'scopes': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['oauth2.Scope']", 'null': 'True', 'blank': 'True'}),
            'tagline': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        }
    }

    complete_apps = ['oauth2']