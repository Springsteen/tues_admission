from django.test import TestCase
from django.http import HttpRequest
from campaigns.views import (
	create_campaign, show_campaign, 
	EMPTY_CAMPAIGN_FIELDS_ERROR,
)
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

	# def test_does_create_campaign_return_error_messages_on_failed_validation(self):
	# 	response = create_campaign(make_POST_request('',''))
	# 	self.assertContains(response.content.decode(), EMPTY_CAMPAIGN_FIELDS_ERROR)	

	def test_does_show_campaign_resolves_the_right_url(self):
		campaign = Campaign.objects.create(title = 'a', description = 'b')
		called = self.client.get('/campaigns/%d/' % (campaign.id,))
		self.assertTemplateUsed(called, 'show_campaign.html')

	def test_does_show_campaign_redirects_home_if_campaign_is_None(self):
		response  = self.client.get('/campaigns/%d/' % (100))
		self.assertTemplateUsed(response, 'home.html')
