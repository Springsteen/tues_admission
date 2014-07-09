from django.shortcuts import render, redirect
from campaigns.models import Campaign, Student
from campaigns.forms import CampaignForm, StudentForm
from django.core.exceptions import ObjectDoesNotExist

EMPTY_CAMPAIGN_FIELDS_ERROR = 'There are validation errors in your submitted form'

def home(request):
	return render(request, 'home.html')

def create_campaign(request):
	form = CampaignForm(data=request.POST)
	if form.is_valid():
		form.save()
		campaign = Campaign.objects.last()
		return redirect(campaign)
	else:
		return render(request, 'new_campaign.html', {'form': form})

def show_campaign(request, campaign_id):
	try:
		campaign = Campaign.objects.get(id = campaign_id)
		students = campaign.student_set.all()
		return render(request, 'show_campaign.html', {'campaign': campaign, 'students': students})
	except ObjectDoesNotExist:
		return render(request, 'home.html')

def list_campaigns(request):
	campaigns = Campaign.objects.all()
	return render(request, 'list_campaigns.html', {'campaigns': campaigns})

def create_student(request, campaign_id):
	form = StudentForm(request.POST)
	if form.is_valid():
		form.save()
		saved_student = Student.objects.last()
		saved_student.campaign = Campaign.objects.get(id=campaign_id)
		saved_student.entry_number = Student.objects.count()
		saved_student.save()
		students = Campaign.objects.get(id=campaign_id).student_set.all()
		return redirect(Campaign.objects.get(id=campaign_id))
	else:
		return render(request, 'create_student.html', {'form': form, 'campaign_id': campaign_id})
