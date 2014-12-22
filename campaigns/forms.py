# -*- coding: utf-8 -*-
from django import forms
from campaigns.models import *

class CampaignForm(forms.models.ModelForm):

    class Meta:
        model = Campaign
        fields = ('title', 'description')
        widgets = {
            'title': forms.fields.TextInput(attrs={
                'class': 'form-control ',
            }),
            'description': forms.fields.TextInput(attrs={
                'class': 'form-control ',
            }),
        }

class HallForm(forms.models.ModelForm):

    class Meta:
        model = Hall
        fields = ('name', 'capacity')
        widgets = {
            'name': forms.fields.TextInput(attrs={
                'class': 'form-control',
            }),
            'capacity': forms.fields.NumberInput(attrs={
                'class': 'form-control',
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
                'class': 'form-control student_field required_field',
            }),
            'second_name': forms.fields.TextInput(attrs={
                'class': 'form-control student_field required_field',
            }),
            'third_name': forms.fields.TextInput(attrs={
                'class': 'form-control student_field required_field',
            }),
            'egn': forms.fields.TextInput(attrs={
                'class': 'form-control student_field required_field',
            }),
            'address': forms.fields.TextInput(attrs={
                'class': 'form-control student_field',
            }),
            'parent_name': forms.fields.TextInput(attrs={
                'class': 'form-control student_field',
            }),
            'parent_number': forms.fields.TextInput(attrs={
                'class': 'form-control student_field',
            }),
            'previous_school': forms.fields.TextInput(attrs={
                'class': 'form-control student_field',
            }),
            'bel_school': forms.fields.NumberInput(attrs={
                'class': 'form-control student_field student_grade_input',
            }),
            'physics_school': forms.fields.NumberInput(attrs={
                'class': 'form-control student_field student_grade_input',
            }),
            'bel_exam': forms.fields.NumberInput(attrs={
                'class': 'form-control student_field student_grade_input',
            }),
            'maths_exam': forms.fields.NumberInput(attrs={
                'class': 'form-control student_field student_grade_input',
            }),
            'maths_tues_exam': forms.fields.NumberInput(attrs={
                'class': 'form-control student_field student_grade_input',
            }),
            'first_choice': forms.fields.TextInput(attrs={
                'class': 'form-control student_field student_choices',
            }),
            'second_choice': forms.fields.TextInput(attrs={
                'class': 'form-control student_field student_choices',
            }),
        }


    # Student personal data validations
    def clean_egn(self):
        egn = self.cleaned_data['egn']
        if Student.objects.filter(egn = egn).count() > 0:
            raise forms.ValidationError(
                'Вече съществува кандидат с ЕГН: %s' % egn
            )
        return egn


    # Student choices validations
    _valid_choices = [ 'СП', 'КМ', '']

    def clean_first_choice(self):
        first_choice = self.cleaned_data['first_choice'].upper()
        if first_choice in self._valid_choices:
            return first_choice
        else:
            raise forms.ValidationError(
                'Невалиден избор на първо желание: %s, моля изберете между КМ и СП или оставете полетата празни' % first_choice
            )

    def clean_second_choice(self):
        second_choice = self.cleaned_data['second_choice'].upper()
        if second_choice in self._valid_choices:
            return second_choice
        else:
            raise forms.ValidationError(
                'Невалиден избор на първо желание: %s, моля изберете между КМ и СП или оставете полетата празни' % second_choice
            )


    # Student grades validations
    def _met_constraints(self, grade):
        if grade == None or grade < 2 or grade > 6:
            return False
        return True

    def clean_bel_school(self):
        bel_school = self.cleaned_data['bel_school']
        if not self._met_constraints(bel_school):
            bel_school = 0.0
        return bel_school

    def clean_bel_exam(self):
        bel_exam = self.cleaned_data['bel_exam']
        if not self._met_constraints(bel_exam):
            bel_exam = 0.0
        return bel_exam

    def clean_maths_exam(self):
        maths_exam = self.cleaned_data['maths_exam']
        if not self._met_constraints(maths_exam):
            maths_exam = 0.0
        return maths_exam

    def clean_maths_tues_exam(self):
        maths_tues_exam = self.cleaned_data['maths_tues_exam']
        if not self._met_constraints(maths_tues_exam):
            maths_tues_exam = 0.0
        return maths_tues_exam

    def clean_physics_school(self):
        physics_school = self.cleaned_data['physics_school']
        if not self._met_constraints(physics_school):
            physics_school = 0.0
        return physics_school
