from django import forms
class CommadForm(forms.Form):
    command = forms.CharField(max_length=200)