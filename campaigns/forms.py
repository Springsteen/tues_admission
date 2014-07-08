from django import forms
from campaigns.models import Campaign

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
        # error_messages = {
        #     'text': {'required': EMPTY_LIST_ERROR}
        # }
