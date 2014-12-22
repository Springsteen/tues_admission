from django.db import models
from django.core.urlresolvers import reverse

class Campaign(models.Model):
    DEFAULT_PK = 1
    title = models.CharField(max_length=40, default='')
    description = models.TextField(max_length=500, default='')

    def get_absolute_url(self):
        return reverse('show_campaign', args=[self.id])

class Hall(models.Model):
    DEFAULT_PK = 1
    campaign = models.ForeignKey(Campaign, default = Campaign.DEFAULT_PK)
    name = models.CharField(max_length=10, default='')
    capacity = models.IntegerField(default=0)

class Student(models.Model):
    campaign = models.ForeignKey(Campaign, default = Campaign.DEFAULT_PK)
    hall = models.ForeignKey(Hall, default = Hall.DEFAULT_PK, blank = True, null=True)
    egn = models.CharField(max_length=10, default='')
    entry_number = models.IntegerField(default=0)
    first_name = models.CharField(max_length=30, default='')
    second_name = models.CharField(max_length=30, default='')
    third_name = models.CharField(max_length=30, default='')

    address = models.CharField(max_length=100, default='', blank=True, null=True)
    parent_name = models.CharField(max_length=100, default='', blank=True, null=True)
    parent_number = models.CharField(max_length=30, default='', blank=True, null=True)
    previous_school = models.CharField(max_length=100, default='', blank=True, null=True)
    bel_school = models.FloatField(default=0, blank=True, null=True)
    physics_school = models.FloatField(default=0, blank=True, null=True)
    bel_exam = models.FloatField(default=0, blank=True, null=True)
    maths_exam = models.FloatField(default=0, blank=True, null=True)
    maths_tues_exam = models.FloatField(default=0, blank=True, null=True)
    first_choice = models.CharField(max_length=2, default='', blank=True, null=True)
    second_choice = models.CharField(max_length=2, default='', blank=True, null=True)

    grades_evaluated = models.FloatField(default=0, blank=True, null=True)

    def get_full_name(self):
        return self.first_name + " " + self.second_name + " " + self.third_name
