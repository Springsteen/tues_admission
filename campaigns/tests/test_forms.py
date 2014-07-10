from django.test import TestCase
from campaigns.forms import CampaignForm
from campaigns.models import Campaign

class CamapaignFormTest(TestCase):
	
	def test_does_form_saves_campaign_objects_with_given_input(self):
		self.assertEqual(Campaign.objects.count(), 0)
		form = CampaignForm(data={
			'title': 'C1',
			'description': 'C1Descr'
		})
		form.save()
		campaign = Campaign.objects.first()
		self.assertEqual(Campaign.objects.count(), 1)
		self.assertEqual(campaign.title, 'C1')
		self.assertEqual(campaign.description, 'C1Descr') 
