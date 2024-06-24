from django import forms
from .models import ShippingAddress

class ShippingForm(forms.ModelForm):
	shipping_full_name = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Contact Name'}), required=True)
	shipping_phone_number = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Contact Number'}), required=True)
	shipping_address1 = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Home Address'}), required=True)
	shipping_address2 = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Builiding or building near '}), required=False)
	shipping_city = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'City e.g Roysambu'}), required=True)
	shipping_county = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'County'}), required=False)

	class Meta:
		model = ShippingAddress
		fields = ['shipping_full_name', 'shipping_phone_number', 'shipping_address1', 'shipping_address2', 'shipping_city', 'shipping_county',]

		exclude = ['user',]
