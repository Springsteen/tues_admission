from django.shortcuts import render
from campaigns.models import Campaign
from campaigns.forms import CampaignForm

def home(request):
	return render(request, 'home.html')

def create_campaign(request):
	form = CampaignForm(data=request.POST)
	if form.is_valid():
		form.save()
		return render(request, 'home.html')
	else:
		return render(request, 'new_campaign.html', {'form': form})
