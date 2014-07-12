from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.http import HttpRequest
from django.test import TestCase
from campaigns.models import Campaign, Student
from campaigns.forms import CampaignForm
from campaigns.views import (
	create_campaign, show_campaign, 
	list_campaigns, create_student,
	show_student, edit_student,
	EMPTY_CAMPAIGN_FIELDS_ERROR,
)

class Base(TestCase):

	def setUp(self):
		User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
		self.user = authenticate(username='john', password='johnpassword')


	def tearDown(self):
		User.objects.get(id = self.user.id).delete()


class HomePageTest(Base):

	def test_does_root_url_resolves_the_home_page(self):
		called = self.client.get('/')
		self.assertTemplateUsed(called, 'home.html')

	def test_does_logout_redirects_to_the_home_page(self):
		response = self.client.get('/logout')
		self.assertRedirects(response, '/')

	def test_does_home_page_does_not_contain_login_form_if_user_is_authenticated(self):
		pass

def make_POST_request_for_campaign(titleValue, descriptionValue, user):
	request = HttpRequest()
	request.method = 'POST'
	request.POST['title'] = titleValue
	request.POST['description'] = descriptionValue
	request.user = user
	return request

class CampaignsViewsTest(Base):

	def test_does_create_campaign_resolves_the_right_url(self):
		self.client.login(username='john', password='johnpassword')
		called = self.client.get('/campaigns/new')
		self.assertTemplateUsed(called, 'new_campaign.html')

	# Trying to do self.client.post was using GET request for some
	# reason so i made it that ugly
	def test_does_create_campaign_saves_objects_with_POST_requests(self):
		self.assertEqual(Campaign.objects.count(), 0)
		create_campaign(make_POST_request_for_campaign('C1', 'C1Descr', self.user))
		campaign = Campaign.objects.first()
		self.assertEqual(Campaign.objects.count(), 1)
		self.assertEqual(campaign.title, 'C1')
		self.assertEqual(campaign.description, 'C1Descr')

	def test_create_campaign_dont_saves_empty_objects(self):
		self.assertEqual(Campaign.objects.count(), 0)
		create_campaign(make_POST_request_for_campaign('', '', self.user))
		self.assertEqual(Campaign.objects.count(), 0)

	def test_create_campaign_redirects_to_show_campaign_on_success(self):
		self.client.login(username='john', password='johnpassword')
		self.assertEqual(Campaign.objects.count(), 0)
		response = self.client.post(
            '/campaigns/new',
            data={'title': 'asd', 'description': 'asdf'}
        )
		campaign = Campaign.objects.first()
		self.assertEqual(Campaign.objects.count(), 1)
		self.assertRedirects(response, '/campaigns/%d/' % campaign.id)

	def test_does_show_campaign_resolves_the_right_url(self):
		self.client.login(username='john', password='johnpassword')
		campaign = Campaign.objects.create(title = 'a', description = 'b')
		called = self.client.get('/campaigns/%d/' % (campaign.id,))
		self.assertTemplateUsed(called, 'show_campaign.html')

	def test_does_show_campaign_redirects_home_if_campaign_is_None(self):
		response  = self.client.get('/campaigns/%d/' % (100))
		self.assertRedirects(response, '/')

	def test_does_show_campaign_list_title_and_description_if_campaign_exist(self):
		self.client.login(username='john', password='johnpassword')
		self.assertEqual(Campaign.objects.count(),0)
		campaign = Campaign.objects.create(title = 'alright', description = 'base')
		self.assertEqual(Campaign.objects.count(),1)
		response = self.client.get('/campaigns/%d/' % (campaign.id))
		self.assertEqual(response.status_code, 200)
		self.assertNotContains(response, 'alright')
		self.assertContains(response, 'base')

	def test_does_show_campaign_lists_all_students_enrolled_in_it(self):
		pass
		# campaign = Campaign.objects.create(title = 'alright', description = 'base')
		# student1 = Student.objects.create()

	def test_does_list_campaigns_resolves_the_right_url(self):
		self.client.login(username='john', password='johnpassword')
		called = self.client.get('/campaigns')
		self.assertTemplateUsed(called, 'list_campaigns.html')

	def test_does_list_campaigns_renders_all_campaigns(self):
		self.assertEqual(Campaign.objects.count(), 0)
		Campaign.objects.create(title = 'first', description='first_d').save()
		Campaign.objects.create(title = 'second', description='second_d').save()
		self.assertEqual(Campaign.objects.count(), 2)
		request = HttpRequest()
		request.user = self.user
		response = list_campaigns(request)
		self.assertContains(response,'first')
		self.assertContains(response,'second_d')

	# def test_does_create_campaign_return_error_messages_on_failed_validation(self):
	# 	response = create_campaign(make_POST_request_for_campaign('',''))
	# 	self.assertContains(response.content.decode(), EMPTY_CAMPAIGN_FIELDS_ERROR)	

def make_POST_request_for_student(user):
	request = HttpRequest()
	request.method = 'POST'
	request.POST['egn'] = 123
	request.POST['first_name'] = 'Asen'
	request.POST['second_name'] = 'Asenov'
	request.POST['third_name'] = 'Asenski'
	request.POST['address'] = 'address'
	request.POST['parent_name'] = 'Asen Asenov'
	request.POST['previous_school'] = 'SOU "ASDF"'
	request.POST['bel_school'] = 3
	request.POST['physics_school'] = 4
	request.POST['bel_exam'] = 5
	request.POST['maths_exam'] = 4
	request.POST['maths_tues_exam'] = 5
	request.POST['first_choice'] = 'SP'
	request.POST['second_choice'] = 'KM'
	request.user = user
	return request

class StudentViewTest(Base):

	def test_does_create_student_resolves_the_right_url(self):
		self.client.login(username='john', password='johnpassword')
		campaign = Campaign.objects.create(title='a', description='b')
		campaign.save()
		called = self.client.get('/campaigns/%d/students/new' % campaign.id)
		self.assertTemplateUsed(called, 'create_student.html')

	def test_does_create_student_saves_new_student_on_POST_request(self):
		campaign = Campaign.objects.create(title='a', description='b')
		self.assertEqual(Student.objects.count(), 0)
		response = create_student(
			make_POST_request_for_student(self.user),
			campaign.id
		)
		self.assertEqual(Student.objects.count(), 1)
		self.assertEqual(
			campaign,
			Student.objects.first().campaign
		)
		self.assertEqual(Student.objects.first().entry_number, 1)
		self.assertEqual(Student.objects.first().first_name, 'Asen')
		self.assertEqual(Student.objects.first().egn, 123)

	def test_does_create_student_gives_students_appropriate_entry_numbers(self):	
		campaign = Campaign.objects.create(title='a', description='b')
		self.assertEqual(Student.objects.count(), 0)
		create_student(
			make_POST_request_for_student(self.user),
			campaign.id
		)
		create_student(
			make_POST_request_for_student(self.user),
			campaign.id
		)
		create_student(
			make_POST_request_for_student(self.user),
			campaign.id
		)
		self.assertEqual(Student.objects.count(), 3)
		students = Student.objects.all()
		for i,s in enumerate(students):
			self.assertEqual(s.entry_number, i+1)	

	def test_does_create_student_redirects_to_the_campaign_he_belongs_to(self):
		self.client.login(username='john', password='johnpassword')
		campaign = Campaign.objects.create(title='a', description='b')
		response = self.client.post(
			'/campaigns/%d/students/new' % campaign.id,
			data={
				'first_name': 'asen', 'second_name': 'asenov',
				'third_name': 'asenski', 'egn': 1234567890,
				'previous_school': 'adsd', 'parent_name': 'adsad',
				'address': 'asda', 'bel_school': 4,
				'physics_school': 5, 'bel_exam': 3,
				'maths_exam': 4, 'maths_tues_exam': 5,
				'first_choice': 'sp', 'second_choice': 'km'
			}
		)	
		self.assertRedirects(response, '/campaigns/%d/' % campaign.id)

	def test_does_show_student_resolves_the_right_url(self):
		self.client.login(username='john', password='johnpassword')
		self.assertEqual(Campaign.objects.count(), 0)
		self.assertEqual(Student.objects.count(), 0)
		campaign = Campaign.objects.create(title='a', description='b')
		student = Student.objects.create(
			campaign=campaign, first_name='Pesho', second_name='Petrov',
			third_name='Popov', egn = 1234567891, entry_number=1
		)
		response = self.client.get('/campaigns/%d/students/%d/' % (campaign.id, student.id))
		self.assertTemplateUsed(response, 'show_student.html')

	def test_does_show_student_lists_appropriate_fields(self):	
		self.assertEqual(Campaign.objects.count(), 0)
		self.assertEqual(Student.objects.count(), 0)
		campaign = Campaign.objects.create(title='a', description='b')
		student = Student.objects.create(
			campaign=campaign, first_name='Pesho', second_name='Petrov',
			third_name='Popov', egn = 1234567891, entry_number=1
		)
		request = HttpRequest()
		request.user = self.user
		response = show_student(request, campaign.id, student.id)
		self.assertContains(response, 'Pesho')
		self.assertContains(response, 'Petrov')
		self.assertContains(response, 'Popov')
		self.assertContains(response, 1234567891)

	def test_does_edit_student_resolves_the_right_url_fields(self):
		self.client.login(username='john', password='johnpassword')
		self.assertEqual(Campaign.objects.count(), 0)
		self.assertEqual(Student.objects.count(), 0)
		campaign = Campaign.objects.create(title='a', description='b')
		student = Student.objects.create(
			campaign=campaign, first_name='Pesho', second_name='Petrov',
			third_name='Popov', egn = 1234567891, entry_number=1
		)
		response = self.client.get('/campaigns/%d/students/%d/edit' % (campaign.id, student.id))
		self.assertTemplateUsed(response, 'edit_student.html')

	def test_does_edit_student_redirects_to_the_root_url_if_ids_does_not_exist(self):
		self.client.login(username='john', password='johnpassword')
		self.assertEqual(Campaign.objects.count(), 0)
		self.assertEqual(Student.objects.count(), 0)
		response = self.client.get('/campaigns/%d/students/%d/edit' % (0, 0))
		self.assertRedirects(response, '/')

	def test_does_edit_student_saves_the_edited_fields_correctly(self):
		self.assertEqual(Campaign.objects.count(), 0)
		self.assertEqual(Student.objects.count(), 0)
		campaign = Campaign.objects.create(title='a', description='b')
		student = Student.objects.create(
			campaign=campaign, first_name='Pesho', second_name='Petrov',
			third_name='Popov', egn = 1234567891, entry_number=1
		)
		response = edit_student(make_POST_request_for_student(self.user), campaign.id, student.id)
		student = Student.objects.get(id = student.id)
		self.assertTemplateUsed(response, 'edit_student.html')
		self.assertEqual(student.first_name, 'Asen')
		self.assertEqual(student.second_name, 'Asenov')
		self.assertEqual(student.third_name, 'Asenski')

	def test_does_create_student_evaluates_the_given_grades_and_saves_the_result(self):
		self.assertEqual(Campaign.objects.count(), 0)
		self.assertEqual(Student.objects.count(), 0)
		campaign = Campaign.objects.create(title='a', description='b')
		create_student(
			make_POST_request_for_student(self.user),
			campaign.id
		)
		saved_student = Student.objects.first()
		self.assertEqual(saved_student.grades_evaluated, 36.0)

	def test_does_create_student_evaluates_the_given_grades_and_saves_the_result(self):
		self.assertEqual(Campaign.objects.count(), 0)
		self.assertEqual(Student.objects.count(), 0)
		campaign = Campaign.objects.create(title='a', description='b')
		create_student(
			make_POST_request_for_student(self.user),
			campaign.id
		)
		saved_student = Student.objects.first()
		request = make_POST_request_for_student(self.user)
		request.POST['bel_school'] = 4
		request.POST['physics_school'] = 5
		edit_student(request, campaign.id, saved_student.id)
		saved_student = Student.objects.get(id = saved_student.id)
		self.assertEqual(saved_student.grades_evaluated, 38.0)





