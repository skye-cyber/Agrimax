from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

from .models import CustomUser, FarmInformation


class CustomRegistrationForm(UserCreationForm):
    username = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(
        max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError("Email is already in use.")
        return email


class FarmInformationForm(forms.ModelForm):
    class Meta:
        model = FarmInformation
        fields = ['farm_name', 'farm_location']  # Remove 'user' from fields
        widgets = {
            'farm_name': forms.TextInput(attrs={
                'class': 'appearance-none block w-full px-4 py-3 border border-gray-300 rounded-lg shadow-lg placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm transition duration-300 ease-in-out transform hover:-translate-y-1',
                'placeholder': 'Enter the name of your farm',
            }),
            'farm_location': forms.TextInput(attrs={
                'class': 'appearance-none block w-full px-4 py-3 border border-gray-300 rounded-lg shadow-lg placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm transition duration-300 ease-in-out transform hover:-translate-y-1',
                'placeholder': 'Enter the location of your farm',
            }),
        }


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class FarmDataForm(forms.Form):
    _N = forms.IntegerField(
        label='Filter recommendations',
        error_messages={
            'required': 'This field is required.',
            'invalid': 'Please enter a valid number (integer or float).'
        }
    )
    model = forms.CharField(
        label='Model',
        error_messages={
            'required': 'This field is required.',
            'invalid': 'Please enter a valid number (integer or float).'
        }

    )
    potassium = forms.CharField(
        label='Potassium Level',
        error_messages={
            'required': 'This field is required.',
            'invalid': 'Please enter a valid number (integer or float).'
        },
        validators=[
            RegexValidator(r'^\d+(\.\d+)?$', 'Please enter a valid number.')
        ]
    )
    phosphorus = forms.CharField(
        label='Phosphorus Level',
        error_messages={
            'required': 'This field is required.',
            'invalid': 'Please enter a valid number (integer or float).'
        },
        validators=[
            RegexValidator(r'^\d+(\.\d+)?$', 'Please enter a valid number.')
        ]
    )
    nitrogen = forms.CharField(
        label='Nitrogen Level',
        error_messages={
            'required': 'This field is required.',
            'invalid': 'Please enter a valid number (integer or float).'
        },
        validators=[
            RegexValidator(r'^\d+(\.\d+)?$', 'Please enter a valid number.')
        ]
    )
    ph = forms.CharField(
        label='PH Level',
        validators=[
            RegexValidator(r'^\d+(\.\d+)?$', 'Please enter a valid number.')
        ],
        error_messages={
            'required': 'This field is required.',
            'invalid': 'Please enter a valid number (integer or float).'
        }
    )
    temperature = forms.CharField(
        label='Temperature',
        error_messages={
            'required': 'This field is required.',
            'invalid': 'Please enter a valid number (integer or float).'
        },
        validators=[
            RegexValidator(r'^\d+(\.\d+)?$', 'Please enter a valid number.')
        ]
    )
    rainfall = forms.CharField(
        label='Rainfall',
        error_messages={
            'required': 'This field is required.',
            'invalid': 'Please enter a valid number (integer or float).'
        },
        validators=[
            RegexValidator(r'^\d+(\.\d+)?$', 'Please enter a valid number.')
        ]
    )
    humidity = forms.CharField(
        label='Humidity',
        error_messages={
            'required': 'This field is required.',
            'invalid': 'Please enter a valid number (integer or float).'
        },
        validators=[
            RegexValidator(r'^\d+(\.\d+)?$', 'Please enter a valid number.')
        ]
    )

    def clean_data_field(self):
        try:
            _N = int(self.cleaned_data['potassium'])
            model = self.cleaned_data['model']
            potassium = float(self.cleaned_data['potassium'])
            phosphorus = float(self.cleaned_data['phosphorus'])
            nitrogen = float(self.cleaned_data['nitrogen'])
            ph = float(self.cleaned_data['ph'])
            temperature = float(self.cleaned_data['temperature'])
            rainfall = float(self.cleaned_data['rainfall'])
            humidity = float(self.cleaned_data['humidity'])

            # Return the float value
            return _N, model, potassium, phosphorus, nitrogen, ph, temperature, rainfall, humidity
        except ValueError:
            raise forms.ValidationError(
                'Please enter a valid number (integer or float).')


class HealthDataForm(forms.Form):
    desired_crop = forms.CharField(
        label='Desired Crop',
        error_messages={
            'required': 'This field is required.',
            'invalid': 'Please enter a valid number (integer or float).'
        }
    )
    potassium = forms.CharField(
        label='Potassium Level',
        error_messages={
            'required': 'This field is required.',
            'invalid': 'Please enter a valid number (integer or float).'
        },
        validators=[
            RegexValidator(r'^\d+(\.\d+)?$', 'Please enter a valid number.')
        ]
    )
    phosphorus = forms.CharField(
        label='Phosphorus Level',
        error_messages={
            'required': 'This field is required.',
        },
        validators=[
            RegexValidator(r'^\d+(\.\d+)?$', 'Please enter a valid number.')
        ]
    )
    nitrogen = forms.CharField(
        label='Nitrogen Level',
        error_messages={
            'required': 'This field is required.',
            'invalid': 'Please enter a valid number (integer or float).'
        },
        validators=[
            RegexValidator(r'^\d+(\.\d+)?$', 'Please enter a valid number.')
        ]
    )
    ph = forms.CharField(
        label='PH Level',
        error_messages={
            'required': 'This field is required.',
            'invalid': 'Please enter a valid number (integer or float).'
        },
        validators=[
            # RegexValidator(r'^[a-zA-Z0-9]+$', 'Please enter a valid alphanumeric
            RegexValidator(r'^\d+(\.\d+)?$', 'Please enter a valid number.')
        ]
    )

    def clean_data_field(self):
        try:
            desired_crop = self.cleaned_data['desired_crop']
            potassium = float(self.cleaned_data['potassium'])
            phosphorus = float(self.cleaned_data['phosphorus'])
            nitrogen = float(self.cleaned_data['nitrogen'])
            ph = float(self.cleaned_data['ph'])

            return desired_crop, potassium, phosphorus, nitrogen, ph  # Return the float value
        except ValueError:
            raise forms.ValidationError(
                'Please enter a valid number (integer or float).')


class LocationForm(forms.Form):
    location = forms.CharField(
        label='Location',
        error_messages={
            'required': 'This field is required.',
            'invalid': 'Please enter the city/location you would like weather forecast for.'
        }
    )

    def clean_data_field(self):
        return str(self.clean_data['location'])
