from django import forms
from campaigns.models import Campaign, Student

class CampaignForm(forms.models.ModelForm):

    class Meta:
        model = Campaign
        fields = ('title', 'description')
        widgets = {
            'title': forms.fields.TextInput(attrs={
                'class': '',
            }),
            'description': forms.fields.TextInput(attrs={
                'class': '',
            }),
        }

class StudentForm(forms.models.ModelForm):

    class Meta:
        model = Student
        fields = (
            'first_name', 'second_name', 'third_name', 
            'egn', 'address', 'parent_name',
            'previous_school', 'bel_school', 'physics_school',
            'bel_exam', 'maths_exam', 'maths_tues_exam',
            'first_choice', 'second_choice', 'parent_number'
        )
        widgets = {
            'first_name': forms.fields.TextInput(attrs={
                'class': 'student_field',
            }),
            'second_name': forms.fields.TextInput(attrs={
                'class': 'student_field',
            }),
            'third_name': forms.fields.TextInput(attrs={
                'class': 'student_field',
            }),
            'egn': forms.fields.TextInput(attrs={
                'class': 'student_field',
            }),
            'address': forms.fields.TextInput(attrs={
                'class': 'student_field',
            }),
            'parent_name': forms.fields.TextInput(attrs={
                'class': 'student_field',
            }),
            'parent_number': forms.fields.TextInput(attrs={
                'class': 'student_field',
            }),
            'previous_school': forms.fields.TextInput(attrs={
                'class': 'student_field',
            }),
            'bel_school': forms.fields.NumberInput(attrs={
                'class': 'student_field student_grade_input',
            }),
            'physics_school': forms.fields.NumberInput(attrs={
                'class': 'student_field student_grade_input',
            }),
            'bel_exam': forms.fields.NumberInput(attrs={
                'class': 'student_field student_grade_input',
            }),
            'maths_exam': forms.fields.NumberInput(attrs={
                'class': 'student_field student_grade_input',
            }),
            'maths_tues_exam': forms.fields.NumberInput(attrs={
                'class': 'student_field student_grade_input',
            }),
            'first_choice': forms.fields.TextInput(attrs={
                'class': 'student_field',
            }),
            'second_choice': forms.fields.TextInput(attrs={
                'class': 'student_field',
            }),
        }
