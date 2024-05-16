from django import forms
from.models import Checkout

class CheckoutRequest(forms.ModelForm):
    class Meta:
        model = Checkout
        fields = ['check_in']
        widgets = {'check_in': forms.HiddenInput()}
       