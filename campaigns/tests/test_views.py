from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.messages.storage.fallback import FallbackStorage
from django.http import HttpRequest
from django.test import TestCase
from campaigns.models import *
from campaigns.forms import *
from campaigns.views import *

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

class HallPopulationTest(Base):

	def test_does_populate_halls_resolves_the_right_url(self):
		self.client.login(username='john', password='johnpassword')
		campaign = Campaign.objects.create(title = 'a', description = 'b')
		hall = Hall.objects.create(name='abv', capacity=50, campaign = campaign)
		called = self.client.get('/campaigns/%d/halls' % campaign.id)
		self.assertTemplateUsed(called, 'populate_halls.html')

	def test_does_populate_halls_renders_show_campaign_if_there_isnt_enough_capacity(self):
		self.client.login(username='john', password='johnpassword')
		campaign = Campaign.objects.create(title = 'a', description = 'b')
		self.assertEqual(campaign.hall_set.count(), 0)
		response = self.client.get('/campaigns/%d/halls' % campaign.id)
		self.assertTemplateUsed(response, 'show_campaign.html')

def build_POST_request(user, args_dict):
	request = HttpRequest()
	request.method = "POST"
	request.user = user
	setattr(request, 'session', 'session')
	messages = FallbackStorage(request)
	setattr(request, '_messages', messages)
	for key in args_dict:
		request.POST[key] = args_dict[key]
	return request

class HallsViewsTest(Base):

	def test_does_create_hall_resolves_the_right_url(self):
		self.client.login(username='john', password='johnpassword')
		campaign = Campaign.objects.create(title = 'a', description = 'b')
		called = self.client.get('/campaigns/%d/halls/new' % campaign.id)
		self.assertTemplateUsed(called, 'create_hall.html')	

	def test_does_create_hall_creates_new_hall_object_with_POST_request(self):
		campaign = Campaign.objects.create(title = 'a', description = 'b')
		self.assertEqual(Hall.objects.count(), 0)
		create_hall(
			build_POST_request(
				self.user,
				{'name': 'hall1', 'capacity': '10'}
			), 
			campaign.id
		)
		self.assertEqual(Hall.objects.count(), 1)

	def test_does_edit_hall_resolves_the_right_url(self):
		self.client.login(username='john', password='johnpassword')
		campaign = Campaign.objects.create(title = 'a', description = 'b')
		hall = Hall.objects.create(name='abv', capacity=50, campaign = campaign)
		called = self.client.get('/campaigns/%d/halls/%d/edit' % (campaign.id, hall.id))
		self.assertTemplateUsed(called, 'edit_hall.html')

	def test_does_edit_hall_saves_edit_fields_correctly(self):
		campaign = Campaign.objects.create(title = 'a', description = 'b')
		self.assertEqual(Hall.objects.count(), 0)
		create_hall(
			build_POST_request(self.user, {'name': 'h1', 'capacity': '10'}),
			campaign.id
		)
		self.assertEqual(Hall.objects.count(), 1)
		hall = Hall.objects.first() 
		edit_hall(
			build_POST_request(self.user, {'name': 'h2', 'capacity': '20'}),
			campaign.id,
			hall.id
		)
		self.assertEqual(Hall.objects.count(), 1)
		hall = Hall.objects.first()
		self.assertEqual(hall.name, 'h2')
		self.assertEqual(hall.capacity, 20)


	def test_does_delete_hall_deletes_the_right_hall(self):
		campaign = Campaign.objects.create(title = 'a', description = 'b')
		self.assertEqual(Hall.objects.count(), 0)
		create_hall(
			build_POST_request(self.user, {'name': 'h1', 'capacity': '10'}),
			campaign.id
		)
		self.assertEqual(Hall.objects.count(), 1)
		hall = Hall.objects.first()
		delete_hall(build_POST_request(self.user, {}), campaign.id, hall.id)
		self.assertEqual(Hall.objects.count(), 0)

	def test_does_delete_hall_doesnt_works_with_other_than_POST_requests(self):
		request = HttpRequest()
		request.method = "GET"
		request.user = self.user
		setattr(request, 'session', 'session')
		messages = FallbackStorage(request)
		setattr(request, '_messages', messages)
		campaign = Campaign.objects.create(title = 'a', description = 'b')
		self.assertEqual(Hall.objects.count(), 0)
		create_hall(
			build_POST_request(self.user, {'name': 'h1', 'capacity': '10'}),
			campaign.id
		)
		self.assertEqual(Hall.objects.count(), 1)
		hall = Hall.objects.first()
		delete_hall(request, campaign.id, hall.id)
		self.assertEqual(Hall.objects.count(), 1)


class CampaignsViewsTest(Base):

	def test_does_create_campaign_resolves_the_right_url(self):
		self.client.login(username='john', password='johnpassword')
		called = self.client.get('/campaigns/new')
		self.assertTemplateUsed(called, 'create_campaign.html')

	# CHECK THE DOCS FOR self.client.post AND TRY MAKING IT WITH THAT METHOD
	def test_does_create_campaign_saves_objects_with_POST_requests(self):
		self.assertEqual(Campaign.objects.count(), 0)
		create_campaign(build_POST_request(self.user, {'title': 'C1', 'description': 'C1Descr'}))
		campaign = Campaign.objects.first()
		self.assertEqual(Campaign.objects.count(), 1)
		self.assertEqual(campaign.title, 'C1')
		self.assertEqual(campaign.description, 'C1Descr')

	def test_create_campaign_dont_saves_empty_objects(self):
		self.assertEqual(Campaign.objects.count(), 0)
		create_campaign(build_POST_request(self.user, {'title': '', 'description': ''}))
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

	def test_does_list_campaigns_resolves_the_right_url(self):
		self.client.login(username='john', password='johnpassword')
		called = self.client.get('/campaigns')
		self.assertTemplateUsed(called, 'list_campaigns.html')

	def test_does_list_campaigns_renders_all_campaigns(self):
		self.assertEqual(Campaign.objects.count(), 0)
		Campaign.objects.create(title = 'first', description='first_d')
		Campaign.objects.create(title = 'second', description='second_d')
		self.assertEqual(Campaign.objects.count(), 2)
		request = HttpRequest()
		request.user = self.user
		response = list_campaigns(request)
		self.assertContains(response,'first')
		self.assertContains(response,'second_d')

	def test_does_delete_campaign_deletes_the_right_campaign(self):
		self.assertEqual(Campaign.objects.count(), 0)
		Campaign.objects.create(title = 'first', description='first_d')
		self.assertEqual(Campaign.objects.count(), 1)
		delete_campaign(
			build_POST_request(self.user, {}), 
			Campaign.objects.first().id
		)
		self.assertEqual(Campaign.objects.count(), 0)
		
	def test_does_delete_campaign_works_only_with_POST_requests(self):
		self.assertEqual(Campaign.objects.count(), 0)
		Campaign.objects.create(title = 'first', description='first_d')
		self.assertEqual(Campaign.objects.count(), 1)
		request = HttpRequest()
		request.method = "GET"
		request.user = self.user
		delete_campaign(request, Campaign.objects.first().id)
		self.assertEqual(Campaign.objects.count(), 1)



sample_student_dict = {
	'egn': '0011223344',
	'first_name': 'Asen',
	'second_name': 'Asenov',
	'third_name': 'Asenski',
	'address': 'ul. Random Randomizer',
	'parent_name': 'Asen Asenov',
	'parent_number': '0123456789',
	'previous_school': 'SOU "Random Randomizer"',
	'bel_school': '3',
	'physics_school': '4',
	'maths_exam': '4',
	'maths_tues_exam': '5',
	'bel_exam': '5',
	'first_choice': 'SP',
	'second_choice': 'KM'
}

class StudentViewTest(Base):

	def test_does_create_student_resolves_the_right_url(self):
		self.client.login(username='john', password='johnpassword')
		campaign = Campaign.objects.create(title='a', description='b')
		campaign.save()
		called = self.client.get('/campaigns/%d/students/new' % campaign.id)
		self.assertTemplateUsed(called, 'create_student.html')

	def test_does_create_student_saves_new_student_on_POST_request(self):
		campaign = Campaign.objects.create(title='a', description='b')
		self.assertEqual(campaign.student_set.count(), 0)
		response = create_student(
			build_POST_request(self.user, sample_student_dict),
			campaign.id
		)
		self.assertEqual(campaign.student_set.count(), 1)
		self.assertEqual(
			campaign,
			Student.objects.first().campaign
		)
		self.assertEqual(campaign.student_set.first().entry_number, 1)
		self.assertEqual(campaign.student_set.first().first_name, 'Asen')
		self.assertEqual(campaign.student_set.first().egn, '0011223344')

	def test_does_create_student_gives_students_appropriate_entry_numbers(self):	
		campaign = Campaign.objects.create(title='a', description='b')
		self.assertEqual(Student.objects.count(), 0)
		create_student(
			build_POST_request(self.user, sample_student_dict),
			campaign.id
		)
		create_student(
			build_POST_request(self.user, sample_student_dict),
			campaign.id
		)
		create_student(
			build_POST_request(self.user, sample_student_dict),
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
				'third_name': 'asenski', 'egn': '1234567890',
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
			third_name='Popov', egn = '1234567891', entry_number=1
		)
		response = self.client.get('/campaigns/%d/students/%d/' % (campaign.id, student.id))
		self.assertTemplateUsed(response, 'show_student.html')

	def test_does_show_student_lists_appropriate_fields(self):	
		self.assertEqual(Campaign.objects.count(), 0)
		self.assertEqual(Student.objects.count(), 0)
		campaign = Campaign.objects.create(title='a', description='b')
		student = Student.objects.create(
			campaign=campaign, first_name='Pesho', second_name='Petrov',
			third_name='Popov', egn = '1234567891', entry_number=1
		)
		request = HttpRequest()
		request.user = self.user
		response = show_student(request, campaign.id, student.id)
		self.assertContains(response, 'Pesho')
		self.assertContains(response, 'Petrov')
		self.assertContains(response, 'Popov')
		self.assertContains(response, '1234567891')

	def test_does_edit_student_resolves_the_right_url_fields(self):
		self.client.login(username='john', password='johnpassword')
		self.assertEqual(Campaign.objects.count(), 0)
		self.assertEqual(Student.objects.count(), 0)
		campaign = Campaign.objects.create(title='a', description='b')
		student = Student.objects.create(
			campaign=campaign, first_name='Pesho', second_name='Petrov',
			third_name='Popov', egn = '1234567891', entry_number=1
		)
		response = self.client.get('/campaigns/%d/students/%d/edit' % (campaign.id, student.id))
		self.assertTemplateUsed(response, 'edit_student.html')

	def test_does_edit_student_redirects_to_the_campaigns_url_if_ids_does_not_exist(self):
		self.client.login(username='john', password='johnpassword')
		self.assertEqual(Campaign.objects.count(), 0)
		self.assertEqual(Student.objects.count(), 0)
		response = self.client.get('/campaigns/%d/students/%d/edit' % (0, 0))
		self.assertRedirects(response, '/campaigns')

	def test_does_edit_student_saves_the_edited_fields_correctly(self):
		self.assertEqual(Campaign.objects.count(), 0)
		self.assertEqual(Student.objects.count(), 0)
		campaign = Campaign.objects.create(title='a', description='b')
		student = Student.objects.create(
			campaign=campaign, first_name='Pesho', second_name='Petrov',
			third_name='Popov', egn = '1234567891', entry_number=1
		)
		response = edit_student(build_POST_request(self.user, sample_student_dict), campaign.id, student.id)
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
			build_POST_request(self.user, sample_student_dict),
			campaign.id
		)
		saved_student = Student.objects.first()
		self.assertEqual(saved_student.grades_evaluated, 36.0)

	def test_does_create_student_evaluates_the_given_grades_and_saves_the_result(self):
		self.assertEqual(Campaign.objects.count(), 0)
		self.assertEqual(Student.objects.count(), 0)
		campaign = Campaign.objects.create(title='a', description='b')
		create_student(
			build_POST_request(self.user, sample_student_dict),
			campaign.id
		)
		saved_student = Student.objects.first()
		request = build_POST_request(self.user, sample_student_dict)
		request.POST['bel_school'] = 4
		request.POST['physics_school'] = 5
		edit_student(request, campaign.id, saved_student.id)
		saved_student = Student.objects.get(id = saved_student.id)
		self.assertEqual(saved_student.grades_evaluated, 38.0)

	def test_does_delete_student_deletes_the_right_student(self):
		self.client.login(username='john', password='johnpassword')
		self.assertEqual(Student.objects.count(), 0)
		campaign = Campaign.objects.create(title='a', description='b')
		create_student(
			build_POST_request(self.user, sample_student_dict),
			campaign.id
		)
		self.assertEqual(Student.objects.count(), 1)
		student = Student.objects.last()
		request = build_POST_request(self.user, {})
		delete_student(request, student.campaign_id, student.id)
		self.assertEqual(Student.objects.count(), 0)

	def test_does_delete_student_deletes_only_if_the_request_method_is_POST(self):
		self.client.login(username='john', password='johnpassword')
		self.assertEqual(Student.objects.count(), 0)
		campaign = Campaign.objects.create(title='a', description='b')
		create_student(
			build_POST_request(self.user, sample_student_dict),
			campaign.id
		)
		self.assertEqual(Student.objects.count(), 1)
		student = Student.objects.last()
		request = HttpRequest()
		request.method = "GET"
		request.user = self.user
		delete_student(request, student.campaign_id, student.id)
		self.assertEqual(Student.objects.count(), 1)
