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
                'class': '',
            }),
            'second_name': forms.fields.TextInput(attrs={
                'class': '',
            }),
            'third_name': forms.fields.TextInput(attrs={
                'class': '',
            }),
            'egn': forms.fields.TextInput(attrs={
                'class': '',
            }),
            'address': forms.fields.TextInput(attrs={
                'class': '',
            }),
            'parent_name': forms.fields.TextInput(attrs={
                'class': '',
            }),
            'parent_number': forms.fields.TextInput(attrs={
                'class': '',
            }),
            'previous_school': forms.fields.TextInput(attrs={
                'class': '',
            }),
            'bel_school': forms.fields.NumberInput(attrs={
                'class': '',
            }),
            'physics_school': forms.fields.NumberInput(attrs={
                'class': '',
            }),
            'bel_exam': forms.fields.NumberInput(attrs={
                'class': '',
            }),
            'maths_exam': forms.fields.NumberInput(attrs={
                'class': '',
            }),
            'maths_tues_exam': forms.fields.NumberInput(attrs={
                'class': '',
            }),
            'first_choice': forms.fields.TextInput(attrs={
                'class': '',
            }),
            'second_choice': forms.fields.TextInput(attrs={
                'class': '',
            }),
        }
