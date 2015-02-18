# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Campaign'
        db.create_table(u'campaigns_campaign', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(default='', max_length=40)),
            ('description', self.gf('django.db.models.fields.TextField')(default='', max_length=500)),
        ))
        db.send_create_signal(u'campaigns', ['Campaign'])

        # Adding model 'Hall'
        db.create_table(u'campaigns_hall', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('campaign', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['campaigns.Campaign'])),
            ('name', self.gf('django.db.models.fields.CharField')(default='', max_length=10)),
            ('capacity', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'campaigns', ['Hall'])

        # Adding model 'Student'
        db.create_table(u'campaigns_student', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('campaign', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['campaigns.Campaign'])),
            ('hall', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['campaigns.Hall'], null=True, blank=True)),
            ('egn', self.gf('django.db.models.fields.CharField')(default='', max_length=10)),
            ('entry_number', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('first_name', self.gf('django.db.models.fields.CharField')(default='', max_length=30)),
            ('second_name', self.gf('django.db.models.fields.CharField')(default='', max_length=30)),
            ('third_name', self.gf('django.db.models.fields.CharField')(default='', max_length=30)),
            ('address', self.gf('django.db.models.fields.CharField')(default='', max_length=100, null=True, blank=True)),
            ('parent_name', self.gf('django.db.models.fields.CharField')(default='', max_length=100, null=True, blank=True)),
            ('parent_number', self.gf('django.db.models.fields.CharField')(default='', max_length=30, null=True, blank=True)),
            ('previous_school', self.gf('django.db.models.fields.CharField')(default='', max_length=100, null=True, blank=True)),
            ('bel_school', self.gf('django.db.models.fields.FloatField')(default=0, null=True, blank=True)),
            ('physics_school', self.gf('django.db.models.fields.FloatField')(default=0, null=True, blank=True)),
            ('bel_exam', self.gf('django.db.models.fields.FloatField')(default=0, null=True, blank=True)),
            ('maths_exam', self.gf('django.db.models.fields.FloatField')(default=0, null=True, blank=True)),
            ('maths_tues_exam', self.gf('django.db.models.fields.FloatField')(default=0, null=True, blank=True)),
            ('first_choice', self.gf('django.db.models.fields.CharField')(default='', max_length=2, null=True, blank=True)),
            ('second_choice', self.gf('django.db.models.fields.CharField')(default='', max_length=2, null=True, blank=True)),
            ('grades_evaluated', self.gf('django.db.models.fields.FloatField')(default=0, null=True, blank=True)),
        ))
        db.send_create_signal(u'campaigns', ['Student'])


    def backwards(self, orm):
        # Deleting model 'Campaign'
        db.delete_table(u'campaigns_campaign')

        # Deleting model 'Hall'
        db.delete_table(u'campaigns_hall')

        # Deleting model 'Student'
        db.delete_table(u'campaigns_student')


    models = {
        u'campaigns.campaign': {
            'Meta': {'object_name': 'Campaign'},
            'description': ('django.db.models.fields.TextField', [], {'default': "''", 'max_length': '500'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '40'})
        },
        u'campaigns.hall': {
            'Meta': {'object_name': 'Hall'},
            'campaign': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': u"orm['campaigns.Campaign']"}),
            'capacity': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '10'})
        },
        u'campaigns.student': {
            'Meta': {'object_name': 'Student'},
            'address': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'bel_exam': ('django.db.models.fields.FloatField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'bel_school': ('django.db.models.fields.FloatField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'campaign': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': u"orm['campaigns.Campaign']"}),
            'egn': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '10'}),
            'entry_number': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'first_choice': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '30'}),
            'grades_evaluated': ('django.db.models.fields.FloatField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'hall': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['campaigns.Hall']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'maths_exam': ('django.db.models.fields.FloatField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'maths_tues_exam': ('django.db.models.fields.FloatField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'parent_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'parent_number': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'physics_school': ('django.db.models.fields.FloatField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'previous_school': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'second_choice': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'second_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '30'}),
            'third_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '30'})
        }
    }

    complete_apps = ['campaigns']
