from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.http import HttpResponse
from django.db import transaction
from campaigns.forms import CampaignForm, StudentForm
from campaigns.models import Campaign, Student, Hall
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import csv

EMPTY_CAMPAIGN_FIELDS_ERROR = 'There are validation errors in your submitted form'

def home(request):
	if request.method == 'GET':
		return render(request, 'home.html')
	else:
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				login(request, user)
				return redirect('/')
			else:
				return redirect('/')
		else:
			return redirect('/')

def logout_user(request):
	logout(request)
	return redirect('/')

@transaction.atomic
def create_campaign(request):
	if request.user.is_authenticated():
		form = CampaignForm(data=request.POST)
		if form.is_valid():
			form.save()
			campaign = Campaign.objects.last()
			return redirect(campaign)
		else:
			return render(request, 'new_campaign.html', {'form': form})
	else:
		return redirect('/')

def show_campaign(request, campaign_id):
	if request.user.is_authenticated():
		try:
			campaign = Campaign.objects.get(id = campaign_id)
			students = campaign.student_set.all()
			return render(request, 'show_campaign.html', {'campaign': campaign, 'students': students})
		except ObjectDoesNotExist:
			return redirect('/')
	else:
		return redirect('/')

def list_campaigns(request):
	if request.user.is_authenticated():
		campaigns = Campaign.objects.all()
		return render(request, 'list_campaigns.html', {'campaigns': campaigns})
	else:
		return redirect('/')

@transaction.atomic
def create_student(request, campaign_id):
	if request.user.is_authenticated():		
		form = StudentForm(request.POST)
		if form.is_valid():
			form.save()
			s = Student.objects.last()
			s.campaign = Campaign.objects.get(id=campaign_id)
			s.entry_number = s.campaign.student_set.count()
			s.grades_evaluated = (
				s.bel_school + s.physics_school + s.bel_exam +
				s.maths_exam + (4 * s.maths_tues_exam) 
			)
			s.save()
			students = Campaign.objects.get(id=campaign_id).student_set.all()
			return redirect(Campaign.objects.get(id=campaign_id))
		else:
			# ADD ERRORS BY CHECKING WHETER THE REQUEST IS POST OR GET
			return render(request, 'create_student.html', {'form': form, 'campaign_id': campaign_id})
	else:
		return redirect('/')

@transaction.atomic
def edit_student(request, campaign_id, student_id):
	if request.user.is_authenticated():	
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
			# very ugly but i know it works
			# TODO - MAKE IT WITH FORM
			student = Student.objects.get(id = student_id)
			student.first_name = request.POST['first_name']
			student.second_name = request.POST['second_name']
			student.third_name = request.POST['third_name']
			student.egn = request.POST['egn']
			student.address = request.POST['address']
			student.previous_school = request.POST['previous_school']
			student.parent_name = request.POST['parent_name']
			student.bel_school = request.POST['bel_school']
			student.physics_school = request.POST['physics_school']
			student.bel_exam = request.POST['bel_exam']
			student.maths_exam = request.POST['maths_exam']
			student.maths_tues_exam = request.POST['maths_tues_exam']
			student.first_choice = request.POST['first_choice']
			student.second_choice = request.POST['second_choice']
			student.grades_evaluated = (
				student.bel_school + student.physics_school + student.bel_exam +
				student.maths_exam + (4 * student.maths_tues_exam) 
			)
			try:	
				student.full_clean()
				student.save()
				return redirect(Campaign.objects.get(id = student.campaign.id))
			except ValidationError:
				# add errors and redirect to back to the form insteed of home
				return redirect('/')
	else:
		return redirect('/')

def show_student(request, campaign_id, student_id):
	if request.user.is_authenticated():	
		campaign = Campaign.objects.get(id = campaign_id)
		student = Student.objects.get(id = student_id)
		return render(request, 'show_student.html', {'campaign': campaign, 'student': student})
	else:
		return redirect('/')

def student_as_pdf(request, campaign_id, student_id):
	if request.user.is_authenticated():	
		response = HttpResponse(content_type='application/pdf')
		response['Content-Disposition'] = ('attachment; filename="%s.pdf"' % student_id)
		student = Student.objects.get(id = student_id)
		enc = 'UTF-8'
		pdfmetrics.registerFont(TTFont('DejaVuSans', 'DejaVuSans.ttf',enc))
		pdfmetrics.registerFont(TTFont('DejaVuSans-Bold', 'DejaVuSans-Bold.ttf',enc))

		p = canvas.Canvas(response)
		p.setFont('DejaVuSans', 12)
		p.drawString(0, 820, 'Входящ номер %d' % student.id)

		p.showPage()
		p.save()
		return response
	else:
		return redirect('/')

def create_hall(request, campaign_id):
	if request.user.is_authenticated():	
		if request.method == 'GET':
			return render(request, 'create_hall.html', {'campaign_id': campaign_id})
		else:
			try:
				hall = Hall.objects.create(
					name=request.POST['name'], 
					capacity=request.POST['capacity']
				)
				hall.campaign = Campaign.objects.get(id = campaign_id)
				hall.save()
				return redirect('/campaigns/%s/' % campaign_id)
			except ValidationError:
				return redirect('/')
	else:
		return redirect('/')

def populate_halls(request, campaign_id):
	if request.user.is_authenticated():
		result = check_for_capacity(
			Campaign.objects.get(id = campaign_id).hall_set.all(),
			Campaign.objects.get(id = campaign_id).student_set.count()
		)
		if result:
			populate(
				Campaign.objects.get(id = campaign_id).hall_set.all(), 
				Campaign.objects.get(id = campaign_id).student_set.all()
			)
			return render(request, 'populate_halls.html', {
				'students' : Campaign.objects.get(id = campaign_id).student_set.all(),
				'campaign_id' : campaign_id
			})
		else:
			return render(request, 'show_campaign.html', {
				'campaign': Campaign.objects.get(id = campaign_id), 
				'students': Campaign.objects.get(id = campaign_id).student_set.all()
			})
	else:
		return redirect('/')

def export_as_csv(request, campaign_id):
	if request.user.is_authenticated():	
		response = HttpResponse(content_type='text/csv')
		response['Content-Disposition'] = 'attachment; filename="database.csv"'
		writer = csv.writer(response)

		campaign = Campaign.objects.get(id = campaign_id)
		students = campaign.student_set.all()	
		
		#Student objects are not itterable so im writing the file this way
		writer.writerow([
		    	'Входящ номер', 'Име', 
		    	'Презиме', 'Фамилия',
		    	'Адрес', 'Имена на родител',
		    	'Училище', 'БЕЛ-Училище',
		    	'Физика-Училище', 'БЕЛ-Матура',
		    	'Математика-Матура', 'Математика-ТУЕС',
		    	'Първо желание', 'Второ желание',
		    	'ЕГН'
		    ])

		for student in students:
			writer.writerow([
		    	student.entry_number, student.first_name, 
		    	student.second_name, student.third_name,
		    	student.address, student.parent_name,
		    	student.previous_school, student.bel_school,
		    	student.physics_school, student.bel_exam,
		    	student.maths_exam, student.maths_tues_exam,
		    	student.first_choice, student.second_choice,
		    	student.egn
		    ])

		return response
	else:
		return redirect('/')


def check_for_capacity(hall_set, students):
	cap = 0
	for h in hall_set:
		cap += h.capacity
	return cap > students

def populate(hall_set, students):
	for i,s in enumerate(students):
		hallIndex = i % hall_set.count()
		while not (hall_set[hallIndex].student_set.count() < hall_set[hallIndex].capacity):
			if hallIndex < hall_set.count():
				hallIndex+=1
			else:
				return
		s.hall = hall_set[hallIndex]
		s.save()



