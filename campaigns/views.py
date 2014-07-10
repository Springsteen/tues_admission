from django.shortcuts import render, redirect
from campaigns.models import Campaign, Student
from campaigns.forms import CampaignForm, StudentForm
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction

EMPTY_CAMPAIGN_FIELDS_ERROR = 'There are validation errors in your submitted form'

def home(request):
	return render(request, 'home.html')

@transaction.atomic
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
		return redirect('/')

def list_campaigns(request):
	campaigns = Campaign.objects.all()
	return render(request, 'list_campaigns.html', {'campaigns': campaigns})

@transaction.atomic
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

def edit_student(request, campaign_id, student_id):
	if request.method == 'GET':
		try:
			student = Student.objects.get(id = student_id)
			campaign = student.campaign
			return render(
				request, 'edit_student.html',
				{'student': student, 'campaign': campaign}
			)
		except ObjectDoesNotExist:
			# add errors
			return redirect('/')
	else:
		student = Student.objects.get(id = student_id)
		student.first_name = request.POST['first_name']
		student.second_name = request.POST['second_name']
		student.third_name = request.POST['third_name']
		student.egn = request.POST['egn']
		print(student.first_name)
		print(student.second_name)
		print(student.third_name)
		print(student.egn)
		print(student.campaign.id)
		print(student.entry_number)
		result = student.save()
		print(result)
		if student.save():
			return redirect(Campaign.objects.get(id = student.campaign.id))
		else:
			return redirect('/')

def show_student(request, campaign_id, student_id):
	campaign = Campaign.objects.get(id = campaign_id)
	student = Student.objects.get(id = student_id)
	return render(request, 'show_student.html', {'campaign': campaign, 'student': student})




