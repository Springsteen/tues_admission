from django.db import models

class Campaign(models.Model):
	title = models.CharField(max_length=40, default='')
	description = models.TextField(max_length=500, default='')
