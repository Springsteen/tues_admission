from django.test import TestCase
from django.http import HttpRequest
from campaigns.views import create_campaign
from campaigns.models import Campaign
from campaigns.forms import CampaignForm

class HomePageTest(TestCase):

	def test_does_root_url_resolves_the_home_page(self):
		called = self.client.get('/')
		self.assertTemplateUsed(called, 'home.html')

class CampaignsViewsTest(TestCase):

	def test_does_create_campaign_resolves_the_right_url(self):
		called = self.client.get('/campaigns/new')
		self.assertTemplateUsed(called, 'new_campaign.html')

	# Trying to do self.client.post was using GET request for some
	# reason so i made it that ugly
	def test_does_create_camapign_saves_objects_with_POST_requests(self):
		self.assertEqual(Campaign.objects.count(), 0)
		request = HttpRequest()
		request.method = 'POST'
		request.POST['title'] = 'C1'
		request.POST['description'] = 'C1Descr'
		create_campaign(request)
		campaign = Campaign.objects.first()
		self.assertEqual(Campaign.objects.count(), 1)
		self.assertEqual(campaign.title, 'C1')
		self.assertEqual(campaign.description, 'C1Descr')

