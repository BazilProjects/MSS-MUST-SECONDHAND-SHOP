from django import forms
from django.forms import modelformset_factory
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "price","image1", "is_new", "is_old"]

# Use `modelformset_factory` instead of `formset_factory` to work with models
ProductFormSet = modelformset_factory(Product, form=ProductForm, extra=1, can_delete=True)


from django import forms
from django.contrib.auth import authenticate
from .models import CustomUser

class SignUpForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ["phone_number", "pin"]

    def clean_pin(self):
        pin = self.cleaned_data.get("pin")
        if len(pin) != 4 or not pin.isdigit():
            raise forms.ValidationError("PIN must be a 4-digit number.")
        return pin

class LoginForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ["phone_number", "pin"]
    def clean(self):
        cleaned_data = super().clean()
        pin = cleaned_data.get("pin")
        if pin and (len(pin) != 4 or not pin.isdigit()):
            raise forms.ValidationError("PIN must be a 4-digit number.")
        return cleaned_data

