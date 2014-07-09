from django import forms
from campaigns.models import Campaign, Student

class CampaignForm(forms.models.ModelForm):

    class Meta:
        model = Campaign
        fields = ('title', 'description')
        widgets = {
            'title': forms.fields.TextInput(attrs={
                'placeholder': 'Enter camapaign title',
                'class': '',
            }),
            'description': forms.fields.TextInput(attrs={
                'placeholder': 'Enter camapaign description',
                'class': '',
            }),
        }

class StudentForm(forms.models.ModelForm):

    class Meta:
        model = Student
        fields = (
            'first_name', 'second_name',
            'third_name', 'egn',
        )
        widgets = {
            'first_name': forms.fields.TextInput(attrs={
                'placeholder': 'Enter student first name',
                'class': '',
            }),
            'second_name': forms.fields.TextInput(attrs={
                'placeholder': 'Enter student second name',
                'class': '',
            }),
            'third_name': forms.fields.TextInput(attrs={
                'placeholder': 'Enter student third name',
                'class': '',
            }),
            'egn': forms.fields.NumberInput(attrs={
                'placeholder': 'Enter student egn',
                'class': '',
            }),
        }
