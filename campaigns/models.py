from django.db import models
from django.core.urlresolvers import reverse

class Campaign(models.Model):
	title = models.CharField(max_length=40, default='')
	description = models.TextField(max_length=500, default='')

	def get_absolute_url(self):
		return reverse('show_campaign', args=[self.id])