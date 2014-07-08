from django.test import TestCase
from django.http import HttpRequest
from campaigns.views import create_campaign
from campaigns.models import Campaign
from campaigns.forms import CampaignForm

def make_POST_request(titleValue, descriptionValue):
	request = HttpRequest()
	request.method = 'POST'
	request.POST['title'] = titleValue
	request.POST['description'] = descriptionValue
	return request

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
	def test_does_create_campaign_saves_objects_with_POST_requests(self):
		self.assertEqual(Campaign.objects.count(), 0)
		create_campaign(make_POST_request('C1', 'C1Descr'))
		campaign = Campaign.objects.first()
		self.assertEqual(Campaign.objects.count(), 1)
		self.assertEqual(campaign.title, 'C1')
		self.assertEqual(campaign.description, 'C1Descr')

	def test_create_campaign_dont_saves_empty_objects(self):
		self.assertEqual(Campaign.objects.count(), 0)
		create_campaign(make_POST_request('', ''))
		self.assertEqual(Campaign.objects.count(), 0)

