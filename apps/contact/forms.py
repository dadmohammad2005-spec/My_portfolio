from django import forms
from .models import ContactMessage

class ContactForm(forms.ModelForm):
    # Honeypot field: hidden in UI, if populated by bots, submission is rejected
    website_hp = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'autocomplete': 'off',
            'tabindex': '-1',
            'aria-hidden': 'true',
            'class': 'hp-field',
            'style': 'display:none !important;'
        })
    )

    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Your Full Name',
                'required': True,
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-input',
                'placeholder': 'name@example.com',
                'required': True,
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'What would you like to discuss?',
                'required': True,
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-textarea',
                'placeholder': 'Write your message here... tell me about your project, timeline, and goals.',
                'rows': 5,
                'required': True,
            }),
        }

    def clean_website_hp(self):
        val = self.cleaned_data.get('website_hp')
        if val:
            raise forms.ValidationError("Bot detected.")
        return val
