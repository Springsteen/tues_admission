from django.shortcuts import render, redirect
from campaigns.models import Campaign
from campaigns.forms import CampaignForm
from django.core.exceptions import ObjectDoesNotExist

EMPTY_CAMPAIGN_FIELDS_ERROR = 'There are validation errors in your submitted form'

def home(request):
	return render(request, 'home.html')

def create_campaign(request):
	form = CampaignForm(data=request.POST)
	if form.is_valid():
		form.save()
		return render(request, 'home.html')
	else:
		return render(request, 'new_campaign.html', {'form': form})

def show_campaign(request, campaign_id):
	try:
		campaign = Campaign.objects.get(id = campaign_id)
		return render(request, 'show_campaign.html', {'campaign': campaign})
	except ObjectDoesNotExist:
		return render(request, 'home.html')