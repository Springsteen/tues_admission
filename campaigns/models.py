from django.db import models
from django.core.urlresolvers import reverse

class Campaign(models.Model):
	DEFAULT_PK = 1
	title = models.CharField(max_length=40, default='')
	description = models.TextField(max_length=500, default='')

	def get_absolute_url(self):
		return reverse('show_campaign', args=[self.id])

class Student(models.Model):
	campaign = models.ForeignKey(Campaign, default = Campaign.DEFAULT_PK)
	egn = models.IntegerField(default=0) 
	entry_number = models.IntegerField(default=0)
	first_name = models.CharField(max_length=30, default='')
	second_name = models.CharField(max_length=30, default='')
	third_name = models.CharField(max_length=30, default='')

	address = models.CharField(max_length=50, default='', blank=True)
	parent_name = models.CharField(max_length=100, default='', blank=True)
	previous_school = models.CharField(max_length=100, default='', blank=True)
	bel_school = models.FloatField(default=0, blank=True)
	physics_school = models.FloatField(default=0, blank=True)
	bel_exam = models.FloatField(default=0, blank=True)
	maths_exam = models.FloatField(default=0, blank=True)
	maths_tues_exam = models.FloatField(default=0, blank=True)
	first_choice = models.CharField(max_length=2, default='', blank=True)
	second_choice = models.CharField(max_length=2, default='', blank=True)