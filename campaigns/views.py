from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.http import HttpResponse
from django.db import transaction

from campaigns.forms import CampaignForm, StudentForm
from campaigns.models import Campaign, Student, Hall

from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from datetime import date

import json

import csv

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
				messages.success(request, "Вие влязохте успешно!")
				return redirect('/campaigns')
			else:
				messages.warning(request, "Този потребител не е активен!")
				return redirect('/')
		else:
			messages.warning(request, "Такъв потребител не съществува!")
			return redirect('/')

def logout_user(request):
	logout(request)
	messages.success(request, "Вие излязохте успешно!")
	return redirect('/')

@transaction.atomic
def create_campaign(request):
	if request.user.is_authenticated():
		form = CampaignForm(data=request.POST)
		if request.method == "POST":
			if form.is_valid():
				form.save()
				campaign = Campaign.objects.last()
				messages.success(
					request, 
					"Вие успешно създадохте кампания с име %s" % campaign.title
				)
				return redirect(campaign)
			else:
				messages.warning(
					request, 
					"Опитът ви беше неуспешен поради това, че името или описанието са твърде дълги"
				)
				return render(request, 'create_campaign.html', {'form': form})
		else:
			return render(request, 'create_campaign.html', {'form': form})
	else:
		messages.warning(
			request,
			"Съдържанието на тази страница не е достъпно за вас поради това, че не сте влязъл в потребителския си акаунт"
		)
		return redirect('/')

@transaction.atomic
def delete_campaign(request, campaign_id):
	if request.user.is_authenticated():
		if request.method == "POST":
			campaign = get_object_or_none(Campaign, id = campaign_id)
			if campaign is not None:
				campaign.delete()
				messages.success(
					request,
					"Вие успешно изтрихте кампания"
				)
				return redirect('/campaigns')
			else:
				messages.warning(
					request,
					"Вие се опитахте да изтриете несъществуваща кампания"
				)
				return redirect('/campaigns')
		else:
			return redirect('/')
	else:
		messages.warning(
			request,
			"Съдържанието на тази страница не е достъпно за вас поради това, че не сте влязъл в потребителския си акаунт"
		)
		return redirect('/')


def show_campaign(request, campaign_id):
	if request.user.is_authenticated():
		campaign = get_object_or_none(Campaign, id = campaign_id)
		if campaign is not None:	
			students = campaign.student_set.order_by("-entry_number").all()
			halls = campaign.hall_set.all()
			return render(
				request, 
				'show_campaign.html', 
				{
					'campaign': campaign, 
					'students': students,
					'halls': halls
				}
			)
		else:
			messages.warning(
				request,
				"Кампанията, която искате да достъпите не съществува"
			)
			return redirect('/campaigns')
	else:
		messages.warning(
			request,
			"Съдържанието на тази страница не е достъпно за вас поради това, че не сте влязъл в потребителския си акаунт"
		)
		return redirect('/')

# EXCEPTION HANDLING, USER AUTHENTICATION
def search_campaign(request, campaign_id):
	campaign = Campaign.objects.get(id = campaign_id)

	result_set = campaign.student_set.all().filter(
		first_name = request.GET['first_name']
	)

	if result_set.count() == 0:
		result_set = campaign.student_set.all().filter(
			egn = request.GET['egn']
		)

	response = {}
	
	if result_set.count() > 0:
		response['status'] = '200'
		response['campaign_id'] = campaign_id
		response['result_set'] = {}
		result_hash = response['result_set']
		for student in result_set:
			result_hash[student.id] = {} 
			result_hash[student.id]['id'] = student.id
			result_hash[student.id]['first_name'] = student.first_name
			result_hash[student.id]['third_name'] = student.third_name
			result_hash[student.id]['egn'] = student.egn
	else:
		response['status'] = '404'
	
	return HttpResponse(json.dumps(response), content_type="application/json")

def list_campaigns(request):
	if request.user.is_authenticated():
		campaigns = Campaign.objects.all()
		return render(request, 'list_campaigns.html', {'campaigns': campaigns})
	else:
		messages.warning(
			request,
			"Съдържанието на тази страница не е достъпно за вас поради това, че не сте влязъл в потребителския си акаунт"
		)
		return redirect('/')

@transaction.atomic
def create_student(request, campaign_id):
	if request.user.is_authenticated():		
		form = StudentForm(request.POST)
		campaign = get_object_or_none(Campaign, id = campaign_id)
		if campaign is not None:	
			if request.method == "POST":
				if form.is_valid():
					form.save()
					s = Student.objects.last()
					student_count = campaign.student_set.count()
					for i in range(student_count+1):
						if get_object_or_none(Student, entry_number = (i+1)) is None:
							s.entry_number = (i+1)
							break
					s.campaign = campaign
					s = validate_grades(s)
					s.grades_evaluated = (
						s.bel_school + s.physics_school + s.bel_exam +
						s.maths_exam + (4 * s.maths_tues_exam) 
					)
					s.save()
					messages.success(request, "Ученикът беше успешно записан.")
					return redirect(campaign)
				else:
					messages.warning(
						request, 
						"Опитът ви беше неуспешен поради това, че сте въвели твърде дълго или невалидно съдържание в някое от полетата"
					)
					return render(request, 'create_student.html', {'form': form, 'campaign_id': campaign_id})
			else:
				return render(request, 'create_student.html', {'form': form, 'campaign_id': campaign_id})
		else:
			return redirect('/campaigns')
	else:
		messages.warning(
			request,
			"Съдържанието на тази страница не е достъпно за вас поради това, че не сте влязъл в потребителския си акаунт"
		)
		return redirect('/')

@transaction.atomic
def edit_student(request, campaign_id, student_id):
	if request.user.is_authenticated():
		student = get_object_or_none(Student, id = student_id)
		campaign = get_object_or_none(Campaign, id = campaign_id)
		if (student is not None) and (campaign is not None):	
			form = StudentForm(request.POST or None, instance = student)
			if request.method == 'GET':
				campaign = student.campaign
				return render(
					request, 'edit_student.html',
					{'form': form, 'student': student, 'campaign': campaign}
				)
			else:
				if form.is_valid():
					form.save()
					student = get_object_or_none(Student, id = student_id)
					if student is not None:	
						student = validate_grades(student)

						student.grades_evaluated = (
							student.bel_school + student.physics_school + student.bel_exam +
							student.maths_exam + (4 * student.maths_tues_exam) 
						)
						student.save()
						messages.success(request, "Вие успешно редактирахте данните на ученика.")
						return redirect(campaign)
					else:
						messages.warning(request, "Ученикът не може да бъде достъпен")
						return redirect(campaign)			
				else:
					messages.warning(
						request, 
						"Опитът ви беше неуспешен поради това, че сте въвели твърде дълго или невалидно съдържание в някое от полетата"
					)
					return render(
						request, 'edit_student.html',
						{'form': form, 'student': student, 'campaign': campaign}
					)
		else:
			messages.warning(request, "Опитахте се да достъпите несъщуствуващ ученик.")
			return redirect('/campaigns')
	else:
		messages.warning(
			request,
			"Съдържанието на тази страница не е достъпно за вас поради това, че не сте влязъл в потребителския си акаунт"
		)
		return redirect('/')

@transaction.atomic
def delete_student(request, campaign_id, student_id):
	if request.user.is_authenticated():
		if request.method == "POST":
			student = get_object_or_none(Student, campaign_id = campaign_id, id = student_id)
			if student is not None:
				student.delete()
				messages.success(
					request,
					"Вие успешно изтрихте ученика"
				)
				return redirect('/campaigns/%s' % campaign_id)
			else:
				messages.warning(
					request,
					"Опитвате се да изтриете несъществуващ ученик"
				)
				return redirect('/campaigns/%s' % campaign_id)
		else:
			return redirect('/')
	else:
		messages.warning(
			request,
			"Съдържанието на тази страница не е достъпно за вас поради това, че не сте влязъл в потребителския си акаунт"
		)
		return redirect('/')


def show_student(request, campaign_id, student_id):
	if request.user.is_authenticated():	
		campaign = get_object_or_none(Campaign, id = campaign_id)
		student = get_object_or_none(Student, id = student_id)
		if (campaign is not None) and (student is not None):
			return render(request, 'show_student.html', {'campaign': campaign, 'student': student})
		else:
			messages.warning(
				request,
				"Ученикът, който искате да достъпите не съществува"
			)
			if campaign is not None:
				return redirect(campaign)
			return redirect('/campaigns')
	else:
		messages.warning(
			request,
			"Съдържанието на тази страница не е достъпно за вас поради това, че не сте влязъл в потребителския си акаунт"
		)
		return redirect('/')

def student_as_pdf(request, campaign_id, student_id):
	if request.user.is_authenticated():	
		student = get_object_or_none(Student, id = student_id)
		campaign = get_object_or_none(Campaign, id = campaign_id)
		if (student is None) or (campaign is None):
			if campaign is not None:
				return redirect(campaign) 
			else:
				return redirect('/campaigns')

		response = HttpResponse(content_type='application/pdf')
		response['Content-Disposition'] = ('attachment; filename="%s.pdf"' % student_id)
		enc = 'UTF-8'
		pdfmetrics.registerFont(TTFont('DejaVuSans', 'DejaVuSans.ttf',enc))
		pdfmetrics.registerFont(TTFont('DejaVuSans-Bold', 'DejaVuSans-Bold.ttf',enc))

		p = canvas.Canvas(response)
		p.setFont('DejaVuSans', 12)
		p.drawString(30, 820, 'Входящ номер %d' % student.entry_number)
		p.drawString(425, 820, 'До Ректора на') 
		p.drawString(425, 805, 'Технически Университет')
		p.drawString(425, 790, 'гр. София')
		p.setFont('DejaVuSans', 20)
		p.drawString(225, 760, 'Заявление')
		p.setFont('DejaVuSans', 10)
		p.drawString(30, 745, 'от %s %s %s' % (student.first_name, student.second_name, student.third_name))
		p.drawString(
			30, 730, 'ученик/чка от VII клас за учебната %s/%s г. на училище: %s' % 
			(date.today().year-1, date.today().year, student.previous_school)
		)
		p.drawString(30, 715, 'живеещ(настящ адрес): %s' % (student.address))
		p.drawString(30, 685, 'Г-н Ректор,')
		p.drawString(30, 670, 'Желая да бъда допуснат/а до състезателен изпит по математика и кандидатстване в')
		p.drawString(30, 655, 'Технологично училище "Електронни системи" към Технически Университет гр. София')
		p.drawString(30, 630, 'Прилагам следните документи:')
		p.drawString(30, 605, '1. Копие на медицинското свидетлество с отразени цветоусещане и диоптри')
		p.drawString(30, 590, '2. Две снимки от настоящата година')
		p.drawString(30, 575, '3. Копие от първата страница на ученическия бележник за 7. клас')
		p.drawString(30, 550, 'Заявявам желания за подредба на специалностите при класирането')
		p.drawString(30, 525, '1. %s' % student.first_choice)
		p.drawString(30, 510, '2. %s' % student.second_choice)
		p.drawString(30, 485, 'Връзка с родител(настойник): %s' % student.parent_name)
		p.drawString(30, 470, 'тел. %s' % student.parent_number)
		d = date.today()
		p.drawString(30, 440, 'гр. София, %s/%s/%s' % (d.day, d.month, d.year))
		p.drawString(390, 465, 'Подпис(на ученика или родителя):')
		p.drawString(390, 435, '................................')
		p.line(0,415,600,415)
		p.setFont('DejaVuSans', 15)
		p.drawString(120, 395, 'Технологично училище "Електронни системи"') 
		p.drawString(140, 380 , 'към Технически Университет гр. София')
		p.setFont('DejaVuSans', 10)
		p.line(60,350,200,350)
		p.line(60,150,200,150)
		p.line(60,350,60,150)
		p.line(200,350,200,150)
		p.setFont('DejaVuSans', 15)
		p.drawString(300, 320 , 'Входящ Nº: %s' % student.entry_number)
		p.drawString(300, 290 , 'Име: %s' % student.first_name)
		p.drawString(300, 260 , 'Презиме: %s' % student.second_name)
		p.drawString(300, 230 , 'Фамилия: %s' % student.third_name)
		p.setFont('DejaVuSans', 10)
		p.drawString(60, 120 , 'Настоящият талон служи за вход в залата за изпита')
		p.drawString(60, 105 , 'Задължително го носете! В противен случай ученикът няма да бъде допуснат до изпита')
		p.drawString(390, 80, 'Приел документите:')
		p.drawString(390, 50, '................................')

		p.showPage()
		p.save()
		return response
	else:
		return redirect('/')

@transaction.atomic
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
		messages.warning(
			request,
			"Съдържанието на тази страница не е достъпно за вас поради това, че не сте влязъл в потребителския си акаунт"
		)
		return redirect('/')

@transaction.atomic
def delete_hall(request, campaign_id, hall_id):
	if request.user.is_authenticated():
		if request.method == "POST":
			hall = get_object_or_none(Hall, campaign_id = campaign_id, id = hall_id)
			campaign = get_object_or_none(Campaign, id = campaign_id)
			if (hall is not None) and (campaign is not None):
				hall.delete()
				messages.success(request, "Вие успешно изтрихте залата")
				return redirect (campaign)
			else:
				messages.warning(request, "Опитахте се да изтриете несъществуваща зала")
				if campaign is not None:
					return redirect(campaign)
				return redirect('/')
		else:
			return redirect('/')
	else:
		messages.warning(
			request,
			"Съдържанието на тази страница не е достъпно за вас поради това, че не сте влязъл в потребителския си акаунт"
		)
		return redirect('/')

@transaction.atomic
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
		messages.warning(
			request,
			"Съдържанието на тази страница не е достъпно за вас поради това, че не сте влязъл в потребителския си акаунт"
		)
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
		messages.warning(
			request,
			"Съдържанието на тази страница не е достъпно за вас поради това, че не сте влязъл в потребителския си акаунт"
		)
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

def validate_grades(student):

	def met_constraints(grade):
		if grade == None or grade < 2 or grade > 6:		
			return False
		return True
	
	if not met_constraints(student.bel_school):
		student.bel_school = 0
	if not met_constraints(student.bel_exam):
		student.bel_exam = 0
	if not met_constraints(student.maths_exam):
		student.maths_exam = 0
	if not met_constraints(student.maths_tues_exam):
		student.maths_tues_exam = 0
	if not met_constraints(student.physics_school):
		student.physics_school = 0

	return student		

def get_object_or_none(model, **kwargs):
	try:
		return model.objects.get(**kwargs)
	except:
		return None
