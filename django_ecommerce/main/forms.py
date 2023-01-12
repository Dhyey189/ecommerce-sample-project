from django import forms
from django.core.exceptions import ValidationError
from rest_apis.models import ProductImage

class CustomerForms(forms.Form):
    name = forms.CharField(max_length=200,required=True)
    email = forms.CharField(max_length=200,required=True)
    password = forms.CharField(max_length=20)
    address = forms.CharField(max_length=1000,required=True)
    mobile = forms.CharField(max_length=12,required=True)

    def clean_address(self):
        address = self.cleaned_data['address']
        if len(address) < 8:
            raise ValidationError("Address must be at least 8 characters")

        return address

    def clean_password(self):
        password = self.cleaned_data['password']
        has_lower_case = False
        has_upper_case = False
        has_special_char = False
        for c in password:
            if c.islower():
                has_lower_case = True
            if c.isupper():
                has_upper_case = True
            if c == '!' or c == '@' or c == '#' or c == '&' or c == '*' or c == '$':
                has_special_char = True
        if len(password) < 8:
            self.add_error('password','password must be at least 8 characters!')
        if not has_lower_case:
            self.add_error('password','Should contain atleat 1 lower case letter!')
        if not has_upper_case:    
            self.add_error('password','Should contain atleat 1 upper case letter!')
        if not has_special_char:
            self.add_error('password','Should contain atleat 1 special characters!')

    # def clean(self):
    #     cleaned_data = super().clean()
    #     address = cleaned_data.post('address')
    #     if len(address) < 8:
    #         raise ValidationError("Address must be at least 8 characters")
    #     return self.cleaned_data


class ProductForm(forms.Form):
    product_name = forms.CharField(max_length=100)
    product_desc = forms.CharField(max_length=1000)
    product_price = forms.CharField()

class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ('product_id','image')



