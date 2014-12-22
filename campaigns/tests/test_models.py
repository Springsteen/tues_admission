from django.test import TestCase
from campaigns.models import Campaign, Student

class CampaignsModelsTest(TestCase):
    pass
    # def test_student_has_all_property_fields(self):
    #   campaign = Campaign.objects.create(title='Camp1', description='Camp1Descr')
    #   campaign.save()
    #   student = Student.objects.create(campaign=campaign)
    #   student.first_name = 'Random'
    #   student.second_name = 'Randomer'
    #   student.third_name = 'Randomizer'
    #   student.egn = '1234567890'
    #   student.save()
    #   new_student = Student.objects.first()
    #   self.assertEqual(new_student.egn, '1234567890')
